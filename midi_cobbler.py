"""
midi_cobbler.py
- convert .mid file to/from .csv 
- transpose pitch in csv domain
- loopback test .mid to .mid
- GPT analysis mode

2024 Chris Derry & ChatGPT
"""

import sys
import argparse

from analyzer import Analyzer
from converter import Converter
from plotter import Plotter
from transformer import Transformer

VERSION = '0.1.0'

parser = argparse.ArgumentParser(
    description="MidiCobbler: A MIDI file conversion and ML analysis tool.")
parser.add_argument('conv_mode', type=str,
    help="Conversion mode ('mid', 'csv', 'loop', 'xform')")
parser.add_argument('input_file', type=str,
    help="Input file")
parser.add_argument('--semitones', type=int, default = 0,
    help="Number of semitones to transpose")
parser.add_argument('--output_file', type=str, default = "loopback.mid",
    help="Output file")
parser.add_argument('--plot', type=bool, default=False,
    help="Enable plotting")

args = parser.parse_args()

conv = Converter(args.input_file,
                args.output_file,
                args.semitones)

if args.plot:
    note_counts, chord_counts = Analyzer.midi_chords(args.input_file)
    print(f"note counts: {note_counts}   chord counts: {chord_counts}")
    Plotter.plot_chords(note_counts, chord_counts)

try:
    if args.conv_mode == "mid":
        conv.midi_to_csv_transpose()
    elif args.conv_mode == "csv":
        conv.csv_to_midi_transpose()
    elif args.conv_mode == "loop":
        conv.midi_loopback()
    elif args.conv_mode == "xform":
        Transformer.pplx_process(conv.midi_to_csv(), Analyzer.midi_chords(args.input_file))
    else:
        print("Invalid mode")
        sys.exit(1)
except Exception:
    print(f"An error occurred: {e}")
    #print("x")

