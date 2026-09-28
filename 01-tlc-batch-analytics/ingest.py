import argparse
import pathlib
import urllib.request
import shutil
import hashlib
from datetime import UTC, datetime
import json

parser = argparse.ArgumentParser(description="Ingest data for batch analytics")
parser.add_argument("--year", help="Input year period", required=True, type=int)
parser.add_argument("--month", help="Input month period", required=True, choices=range(1, 13), type=int)
args = parser.parse_args()
print(f"Ingesting data for year: {args.year}, month: {args.month:02d}")

filename = f"yellow_tripdata_{args.year}-{args.month:02d}.parquet"
print(f"Constructed file name: {filename}")

# https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2026-01.parquet

url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{filename}"
print(f"Constructed URL: {url}")

project_dir = pathlib.Path(__file__).resolve().parent
raw_dir = project_dir / "data" / "raw"
raw_dir.mkdir(parents=True, exist_ok=True)

final_path = raw_dir / filename
temp_filename = f"{filename}.part"
temp_path = raw_dir / temp_filename

retrieved_at_utc = None
fingerprint = None

def write_manifest(manifest_path, manifest):
    temp_manifest_path = manifest_path.with_name(manifest_path.name + ".tmp")
    try:
        with temp_manifest_path.open("w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=4)
        temp_manifest_path.replace(manifest_path)
    except Exception as e:
        if temp_manifest_path.exists():
            temp_manifest_path.unlink()
        print(f"Error occurred while writing manifest {manifest_path}: {e}")
        raise

# If the final file already exists, print a message and skip downloading.
if pathlib.Path(final_path).exists():
    print(f"File {filename} already exists. Skipping download.")
    fingerprint = None
    retrieved_at_utc = None
    # 2. Existing data file, no manifest: write the metadata you can establish now, keeping the unknown retrieval time as null.
    manifest_path = final_path.with_suffix(".manifest.json")
    if not manifest_path.exists():
        with final_path.open("rb") as file:
            fingerprint = hashlib.file_digest(file, "sha256").hexdigest()
        manifest = {"source_url": url, "retrieved_at_utc": retrieved_at_utc, "file_size_bytes": final_path.stat().st_size, "sha256": fingerprint}
        write_manifest(manifest_path, manifest)
    # 3. Existing data file and manifest: load the saved manifest. Compare its URL, size, and checksum with your current values.
    #    - If they match, reuse the saved manifest, preserving its original retrieval timestamp.
    #    - If they differ, raise an error describing the mismatch. This prevents silently accepting a changed local file.
    with open(manifest_path, "r", encoding="utf-8") as f:
        saved_manifest = json.load(f)
        if saved_manifest["source_url"] != url:
            raise ValueError(f"Source URL mismatch: expected {url}, found {saved_manifest['source_url']}")
        if saved_manifest["file_size_bytes"] != final_path.stat().st_size:
            raise ValueError(f"File size mismatch: expected {final_path.stat().st_size}, found {saved_manifest['file_size_bytes']}")
        with final_path.open("rb") as f:
            current_fingerprint = hashlib.file_digest(f, "sha256").hexdigest()
        if saved_manifest["sha256"] != current_fingerprint:
            raise ValueError(f"SHA256 hash mismatch: expected {current_fingerprint}, found {saved_manifest['sha256']}")
        manifest = saved_manifest
else:
    try:
        # Download the file to a temporary location first.
        with urllib.request.urlopen(url, timeout=30) as response, open(temp_path, 'wb') as out_file:
            expectedSize = response.headers.get("Content-Length")
            shutil.copyfileobj(response, out_file)
        # Check size after the output is closed and buffered bytes are flushed.
        downloadedSize = temp_path.stat().st_size
        if expectedSize is not None and downloadedSize != int(expectedSize):
            raise ValueError(f"Downloaded file size {downloadedSize} does not match expected size {expectedSize}.")
        # After the download succeeds and the file is closed, rename it to the final .parquet filename.
        shutil.move(temp_path, final_path)
        print(f"Downloaded and saved as {filename}")
        retrieved_at_utc = datetime.now(UTC).isoformat()
        manifest_path = final_path.with_suffix(".manifest.json")
        # 1. After a new download: write the new metadata, including its retrieval timestamp.
        with final_path.open("rb") as f:
            fingerprint = hashlib.file_digest(f, "sha256").hexdigest()
            print(f"SHA256 hash of the downloaded file: {fingerprint}")
        manifest = {"source_url": url, "retrieved_at_utc": retrieved_at_utc, "file_size_bytes": final_path.stat().st_size, "sha256": fingerprint}
        write_manifest(manifest_path, manifest)
    except Exception as e:
        # If downloading fails, remove the temporary file and report the error.
        if temp_path.exists():
            temp_path.unlink()
        print(f"Error occurred while downloading {url}: {e}")
        raise
