# Virtual Piano To Midi
 Converts virtual piano notes (using virtualpiano.net semantics) to a midi file

## Installation

Use the package manager pip to install the requirements (only one for now, but may require more later)
```bash
pip install -r requirements.txt
```

## Usage

Create your own virtual piano sheet or use one from [Virtual Piano](https://virtualpiano.net/) or [vpsheets](https://vp-sheets.fly.dev/) and paste it into the text box. Adjust timing using the tempo and rest semantics as needed. Press "Generate Midi" and play your song!

## Semantics

' - One beat rest

| - One second rest

[asdf] - Notes are played together simultaneously

## Contribution

Pull requests are welcome. Please open an issue with any problems.