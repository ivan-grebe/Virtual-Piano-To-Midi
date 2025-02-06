# Virtual Piano To Midi
 Converts virtual piano notes (using virtualpiano.net semantics) to a midi file

## Installation

Use the package manager pip to install the requirements (only one for now, but may require more later)
```bash
pip install -r requirements.txt
```

## Usage

Navigate to the installed folder in your command prompt and run
```bash
python vp_to_midi.py
```

Create your own virtual piano sheet or use one from [Virtual Piano](https://virtualpiano.net/) or [vpsheets](https://vp-sheets.fly.dev/) and paste it into the text box. Adjust timing using the tempo and rest semantics as needed. Press "Generate Midi" and play your song!

## Semantics

' - One beat rest

| - One second rest

[asdf] - Notes are played together simultaneously

TEMPO:xxx - Insert to wherever you want a tempo change

Examples shown in demo file. Try and guess what song it is!

## Contribution

Pull requests are welcome. Please open an issue with any problems.
