"""Offline behavior checks for the ingestion command: python -m unittest discover -s tests -v."""

import contextlib
import http.client
import io
from pathlib import Path
import runpy
import shutil
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from urllib.error import HTTPError


PROJECT_DIR = Path(__file__).resolve().parents[1]
FILENAME = "yellow_tripdata_2024-01.parquet"
SOURCE_URL = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{FILENAME}"


class IngestTests(unittest.TestCase):
    def setUp(self):
        workspace = tempfile.TemporaryDirectory(prefix="tlc-ingest-test-")
        self.root = Path(workspace.name).resolve()
        # Cleanup is restricted to the temporary directory created for this test.
        self.assertTrue(self.root.is_relative_to(Path(tempfile.gettempdir()).resolve()))
        self.addCleanup(workspace.cleanup)
        self.project = self.root / "project"
        self.project.mkdir()
        self.script = self.project / "ingest.py"
        shutil.copyfile(PROJECT_DIR / "ingest.py", self.script)
        self.launch_dir = self.root / "launch"
        self.launch_dir.mkdir()
        self.final_path = self.project / "data" / "raw" / FILENAME

    def http_response(self, body, headers=None):
        """Use Python's actual HTTP reader, backed by memory instead of a socket."""
        if headers is None:
            headers = {"Content-Length": str(len(body))}
        header_lines = "".join(f"{name}: {value}\r\n" for name, value in headers.items())
        wire_bytes = f"HTTP/1.1 200 OK\r\n{header_lines}\r\n".encode("ascii") + body
        socket = SimpleNamespace(makefile=lambda mode: io.BytesIO(wire_bytes))
        response = http.client.HTTPResponse(socket)
        self.addCleanup(response.close)
        response.begin()
        return response

    def run_ingest(self, response=None, *, error=None, args=None):
        if args is None:
            args = ["--year", "2024", "--month", "1"]
        # A copied script keeps __file__ inside the test's temporary project.
        # Launch elsewhere to catch accidental dependence on the working directory.
        with (
            contextlib.chdir(self.launch_dir),
            patch.object(sys, "argv", [str(self.script), *args]),
            patch("urllib.request.urlopen", return_value=response, side_effect=error) as request,
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(io.StringIO()),
        ):
            runpy.run_path(str(self.script), run_name="__main__")
        return request

    def assert_no_download_files(self):
        self.assertFalse(self.final_path.exists())
        self.assertEqual(list(self.root.rglob("*.part")), [])

    def test_success_saves_response_in_project_raw_directory(self):
        body = b"sample source bytes"
        response = self.http_response(body)
        request = self.run_ingest(response)

        request.assert_called_once_with(SOURCE_URL, timeout=30)
        self.assertEqual(self.final_path.read_bytes(), body)
        self.assertEqual(list(self.root.rglob("*.part")), [])
        self.assertEqual(list(self.launch_dir.iterdir()), [])
        self.assertTrue(response.closed)

    def test_rerun_preserves_existing_file_without_an_http_request(self):
        body = b"original source bytes"
        self.run_ingest(self.http_response(body))
        request = self.run_ingest(error=AssertionError("A rerun must skip the request"))

        request.assert_not_called()
        self.assertEqual(self.final_path.read_bytes(), body)
        self.assertEqual(list(self.root.rglob("*.part")), [])

    def test_interrupted_download_removes_partial_file_and_raises(self):
        response = self.http_response(b"sample source bytes")
        with patch.object(response, "read", side_effect=[b"partial bytes", OSError("connection lost")]):
            with self.assertRaisesRegex(OSError, "connection lost"):
                self.run_ingest(response)

        self.assert_no_download_files()
        self.assertTrue(response.closed)

    def test_http_404_leaves_no_download_and_raises(self):
        error = HTTPError(SOURCE_URL, 404, "Not Found", {}, None)
        with self.assertRaises(HTTPError):
            self.run_ingest(error=error)
        self.assert_no_download_files()

    def test_timeout_leaves_no_download_and_raises(self):
        with self.assertRaises(TimeoutError):
            self.run_ingest(error=TimeoutError("request timed out"))
        self.assert_no_download_files()

    def test_response_without_content_length_can_be_saved(self):
        body = b"source without a declared size"
        self.run_ingest(self.http_response(body, headers={}))
        self.assertEqual(self.final_path.read_bytes(), body)
        self.assertEqual(list(self.root.rglob("*.part")), [])

    def test_truncated_response_is_rejected_and_removed(self):
        # A sized HTTP read can return EOF without raising for a short body.
        response = self.http_response(b"short body", headers={"Content-Length": "100"})
        with self.assertRaises(ValueError):
            self.run_ingest(response)
        self.assert_no_download_files()

    def test_invalid_arguments_are_rejected(self):
        cases = [
            ["--year", "2024", "--month", "0"],
            ["--year", "2024", "--month", "13"],
            ["--year", "abc", "--month", "1"],
            ["--year", "2024"],
            ["--month", "1"],
        ]
        for args in cases:
            with self.subTest(args=args):
                with self.assertRaises(SystemExit) as result:
                    self.run_ingest(args=args, error=AssertionError("Invalid arguments must skip HTTP"))
                self.assertEqual(result.exception.code, 2)
                self.assert_no_download_files()


if __name__ == "__main__":
    unittest.main()
