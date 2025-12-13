# TTS (Text-to-Speech) — Setup and usage

This project converts text files to audio using the `mac-tts` scripts.

## Virtualenv / Python

- This repo expects a project virtual environment named `venv` in the project root or the older `bin` layout. Scripts in this project prefer an explicit interpreter path and will refuse to run if no venv is found.
-- To create a venv (macOS / Homebrew Python):

```bash
python3 -m venv ./venv
source ./venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Or install `requests` directly into the venv:

```bash
./venv/bin/python -m pip install requests
```

## Running the conversion script

-- To run the multi-file conversion script (uses `./venv/bin/python` explicitly if present):

```bash
./converttext.sh
```

-- The script will use `./venv/bin/python` or `./bin/python` if present, otherwise if the shell has an activated venv it uses `python3`. If none is available it stops with a helpful message.

Note: `converttext.sh` explicitly runs the python interpreter it finds and does not automatically create a venv. It also excludes `requirements.txt`, `README*`, and files ending with `.done` from processing.

## Running single files

- To run a single file with the project venv explicitly:

```bash
./venv/bin/python mac-tts.py path/to/textfile.txt
```

## Troubleshooting

- If you need to change the interpreter `converttext.sh` uses, edit the script's `PYTHON` detection logic or run `./venv/bin/python mac-tts.py` directly.

- If you see `ModuleNotFoundError: No module named 'requests'`, install `requests` into the venv (see commands above).
- If you accidentally have a file named `requests.py` in the project root, rename it — it will shadow the external package.

## Notes

- The script uses `ffmpeg` (Homebrew recommended) for audio conversion. Install it with `brew install ffmpeg` if missing.
