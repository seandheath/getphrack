#!/usr/bin/env python3

import argparse
import glob
import os
import shutil
import tarfile
import urllib.request
import urllib.error


def download_issues():
    opener = urllib.request.build_opener()
    opener.addheaders = [("User-Agent", "Wget/1.21")]
    i = 1
    while True:
        filename = f"phrack{i}.tar.gz"
        url = f"http://phrack.org/archives/tgz/{filename}"
        try:
            resp = opener.open(url)
            with open(filename, "wb") as f:
                f.write(resp.read())
            print(f"\rDownloaded issue {i}", end="", flush=True)
            i += 1
        except urllib.error.HTTPError:
            break
    print(f"\rDownloaded {i - 1} issues")


def extract_issues():
    for f in sorted(glob.glob("phrack[0-9]*.tar.gz")):
        name = os.path.splitext(os.path.splitext(f)[0])[0]
        dest = os.path.join("phrack", name)
        os.makedirs(dest, exist_ok=True)
        with tarfile.open(f) as tar:
            tar.extractall(path=dest, filter="data")
        os.remove(f)


def combine_articles():
    extracted = False
    if not os.path.isdir("phrack"):
        if not os.path.isfile("phrack.tar.gz"):
            print("No archive or phrack/ directory found")
            return
        with tarfile.open("phrack.tar.gz") as tar:
            tar.extractall(filter="data")
        extracted = True
    separator = "=" * 79
    files = sorted(
        glob.glob("phrack/phrack*/[0-9]*.txt"),
        key=lambda p: (
            int(os.path.basename(os.path.dirname(p)).removeprefix("phrack")),
            int(os.path.splitext(os.path.basename(p))[0]),
        ),
    )
    if not files:
        print("No articles to combine")
    else:
        with open("phrack.txt", "w") as out:
            for i, path in enumerate(files):
                parts = path.split(os.sep)
                issue = int(parts[1].removeprefix("phrack"))
                article = int(os.path.splitext(parts[2])[0])
                if i > 0:
                    out.write("\n")
                out.write(f"{separator}\n")
                out.write(f"PHRACK ISSUE {issue} - ARTICLE {article}\n")
                out.write(f"{separator}\n\n")
                with open(path, "r", errors="replace") as f:
                    out.write(f.read())
        print(f"Combined {len(files)} articles into phrack.txt")
    if extracted:
        shutil.rmtree("phrack")


def create_archive():
    if not os.path.isdir("phrack"):
        print("No issues to archive")
        return
    with tarfile.open("phrack.tar.gz", "w:gz") as tar:
        tar.add("phrack")
    shutil.rmtree("phrack")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download and archive Phrack issues")
    parser.add_argument("--skip-download", action="store_true", help="Skip downloading, just extract and archive")
    parser.add_argument("--combine", action="store_true", help="Combine all articles into phrack.txt")
    args = parser.parse_args()

    if not args.skip_download:
        download_issues()
    extract_issues()
    if args.combine:
        combine_articles()
    create_archive()
