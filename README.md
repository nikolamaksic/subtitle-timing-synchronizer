# Subtitle Timing Synchronizer

Subtitle Timing Synchronizer is a simple tool that helps fix delayed or out-of-sync subtitles by shifting the timing of subtitle lines. It currently supports `.srt` files and allows you to apply a consistent delay or advance to all subtitle entries.

## Installation

Before using the tool, make sure to install the required Python packages:

    pip install -r requirements.txt

## How to Use

You can now run the script with command-line arguments to specify the delay, input file, and optional mode and start time:

    python main.py --start 00:20:002 --delay 00:52:002 --mode delay --input examples\example_subtitle.srt 

### Arguments

- `--start` — the time **after** which the delay should begin (format: MM:SS:MS).
  Example: `00:20:002` means start applying delay after 20 seconds and 2 milliseconds.

- `--delay` — the amount of time to delay each subtitle line (format: MM:SS:MS).
  Example: `00:52:002` adds 52 seconds and 2 milliseconds to each subtitle that starts after the given `--start`.

- `--mode` — either `delay` (default) to push subtitles later or `advance` to shift them earlier.
  Example: `--mode advance` will subtract the delay instead of adding it.

- `--input` — path to the `.srt` subtitle file.
- `--output` *(optional)* — custom output path. If omitted, a file with `_fixed` will be created in the same folder.

### Example

    python main.py --start 00:20:002 --delay 00:52:002 --input examples\example_subtitle.srt --mode advance

This applies a 52.002s delay to all subtitles starting after 20.002s and because of `--mode advance` it will subtract start and end time of subtitles.

## TODO

- Add command-line argument support for input, output, and delay values ✅
- Create a simple user interface (UI) for adjusting subtitle timings
- Support negative delay (advance subtitles instead of delaying) ✅
- Add a start time for delaying subtitles if they are not out of sync from the beginning of the video ✅
- (*Still not decided if it will be part of repo or not) Fix wrongly formatted characters like: `�` → `š`, `đ`, etc.

## Why use this?

If your subtitle file is slightly out of sync with your video - either too early or too late – this tool makes it quick and easy to correct that.
