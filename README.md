# Phrack Archive

Download and archive all issues of [Phrack Magazine](http://phrack.org).

## Usage

```
python getphrack.py
```

This downloads all available issues, extracts them into `phrack/`, and packages everything into `phrack.tar.gz`.

### Options

| Flag | Description |
|------|-------------|
| `--skip-download` | Skip downloading, just extract and archive existing tarballs |
| `--combine` | Combine all articles into a single `phrack.txt` file |

### Examples

Download, combine into one file, and archive:

```
python download.py --combine
```

Re-extract and combine without re-downloading:

```
python download.py --skip-download --combine
```
