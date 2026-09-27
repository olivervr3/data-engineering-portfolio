import argparse
import pathlib
import urllib.request
import shutil

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

# If the final file already exists, print a message and skip downloading.
if pathlib.Path(final_path).exists():
    print(f"File {filename} already exists. Skipping download.")
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
    except Exception as e:
        # If downloading fails, remove the temporary file and report the error.
        if temp_path.exists():
            temp_path.unlink()
        print(f"Error occurred while downloading {url}: {e}")
        raise
