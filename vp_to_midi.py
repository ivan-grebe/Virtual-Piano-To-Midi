#!/usr/bin/env python

from mido import Message, MidiFile, MidiTrack, MetaMessage 
import tkinter as tk
from tkinter import messagebox

# --- 61 key piano mapping ---

# row 1: white keys and black keys
row1_white = {
    '1': 36,  # C2
    '2': 38,  # D2
    '3': 40,  # E2
    '4': 41,  # F2
    '5': 43,  # G2
    '6': 45,  # A2
    '7': 47,  # B2
    '8': 48,  # C3
    '9': 50,  # D3
    '0': 52   # E3
}
row1_black = {
    '!': 37,  # C#2
    '@': 39,  # D#2
    '$': 42,  # F#2 (shifted 4)
    '%': 44,  # G#2 (shifted 5)
    '^': 46,  # A#2 (shifted 6)
    '*': 49,  # C#3 (shifted 8)
    '(': 51   # D#3 (shifted 9)
}

# row 2 (q to p): white keys and black keys
row2_white = {
    'q': 53,  # F3
    'w': 55,  # G3
    'e': 57,  # A3
    'r': 59,  # B3
    't': 60,  # C4
    'y': 62,  # D4
    'u': 64,  # E4
    'i': 65,  # F4
    'o': 67,  # G4
    'p': 69   # A4
}
row2_black = {
    'Q': 54,  # F#3
    'W': 56,  # G#3
    'E': 58,  # A#3
    'T': 61,  # C#4
    'Y': 63,  # D#4
    'I': 66,  # F#4
    'O': 68,  # G#4
    'P': 70   # A#4
}

# row 3 (a to l): white keys and black keys
row3_white = {
    'a': 71,  # B4
    's': 72,  # C5
    'd': 74,  # D5
    'f': 76,  # E5
    'g': 77,  # F5
    'h': 79,  # G5
    'j': 81,  # A5
    'k': 83,  # B5
    'l': 84   # C6
}
row3_black = {
    'S': 73,  # C#5
    'D': 75,  # D#5
    'G': 78,  # F#5
    'H': 80,  # G#5
    'J': 82   # A#5
}

# row 4 (z to m): white keys and black keys
row4_white = {
    'z': 86,  # D6
    'x': 88,  # E6
    'c': 89,  # F6
    'v': 91,  # G6
    'b': 93,  # A6
    'n': 95,  # B6
    'm': 96   # C7
}
row4_black = {
    'Z': 87,  # D#6
    'C': 90,  # F#6
    'V': 92,  # G#6
    'B': 94   # A#6
}

# merge all the mappings
key_mapping = {}
for mapping in (row1_white, row1_black, row2_white, row2_black,
                row3_white, row3_black, row4_white, row4_black):
    key_mapping.update(mapping)

# parser
def parse_virtual_piano(sheet: str):
    sheet = sheet.replace('-', ' ')  # treat '-' as space
    events = []
    tokens = sheet.split()
    
    for token in tokens:
        if token.startswith("TEMPO:"):
            try:
                bpm_str = token.split(":")[1]
                new_bpm = int(bpm_str)
                if new_bpm <= 0:
                    raise ValueError("BPM must be positive")
                events.append({
                    'type': 'tempo',
                    'tempo': 60000000 // new_bpm  # microseconds per beat
                })
            except:
                pass
        elif token == "|":  # long rest
            events.append({'type': 'rest', 'delay': 600})
        elif token == "'":  # short rest
            events.append({'type': 'rest', 'delay': 120})
        elif token.startswith('[') and token.endswith(']'):
            chord = [key_mapping[ch] for ch in token[1:-1] if ch in key_mapping]
            events.append({'type': 'note', 'notes': chord, 'delay': 200})
        else:
            notes = [key_mapping[ch] for ch in token if ch in key_mapping]
            if notes:
                events.append({'type': 'note', 'notes': notes, 'delay': 200})
    return events

# midi creation
def create_midi(sheet: str, filename: str = "output.mid"):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    
    # initial tempo (100 BPM)
    current_tempo = 600000  # 60000000 / 100
    track.append(MetaMessage('set_tempo', tempo=current_tempo, time=0))
    
    for event in parse_virtual_piano(sheet):
        if event['type'] == 'tempo':
            current_tempo = event['tempo']
            track.append(MetaMessage('set_tempo', tempo=current_tempo, time=0))
        elif event['type'] == 'note':
            notes = event['notes']
            delay = event['delay']
            
            if notes:
                # note on for all notes
                for note in notes:
                    track.append(Message('note_on', note=note, velocity=64, time=0))
                # note off with delay on the first note
                track.append(Message('note_off', note=notes[0], velocity=64, time=delay))
                for note in notes[1:]:
                    track.append(Message('note_off', note=note, velocity=64, time=0))
        elif event['type'] == 'rest':
            # rest = just advance time
            track.append(MetaMessage('track_name', name='', time=event['delay']))
    
    mid.save(filename)
    messagebox.showinfo("Success", f"MIDI file saved as {filename}")

# gui
def open_gui():
    def submit():
        sheet = text_box.get("1.0", tk.END).strip()
        if sheet:
            try:
                create_midi(sheet, "song.mid")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    root = tk.Tk()
    root.title("Virtual Piano to MIDI")
    
    tk.Label(root, text="Enter Virtual Piano Sheet:").pack(pady=5)
    text_box = tk.Text(root, width=80, height=20)
    text_box.pack(pady=5)
    
    tk.Button(root, text="Generate MIDI", command=submit).pack(pady=5)
    tk.Button(root, text="Exit", command=root.quit).pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    open_gui()
