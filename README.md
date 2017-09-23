# wav2Collage

Project for `MUSIC 3310`.  Generating a collage from a `*.wav` file.

## Setup

Assuming you have [`virtualenv`](https://virtualenv.pypa.io/en/stable/) installed:

```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## How to run

Place a `*.wav` file at the root of the directory.  Then, run the following:

```bash
python src/main.py ./*.wav
```

This will generate a `collage.png` file.
