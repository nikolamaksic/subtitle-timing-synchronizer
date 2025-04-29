# Subtitle Timing Synchronizer

Subtitle Timing Synchronizer is a simple tool that helps fix delayed or out-of-sync subtitles by shifting the timing of subtitle lines. It currently supports `.srt` files and allows you to apply a consistent delay or advance to all subtitle entries.

## How to Use (currently)

Run the script directly with Python:

    python main.py

The delay settings are hardcoded for now, inside the script, like this:

    title_delay = (0, 0, 1500)  # (minutes, seconds, milliseconds)  - e.g. adds 1.5 seconds to all subtitle lines

The output will be saved as a new file with "_fixed" added to the name.

## TODO

- Add command-line argument support for input, output, and delay values
- Create a simple user interface (UI) for adjusting subtitle timings
- Support negative delay (advance subtitles instead of delaying)
- Add a start time for delaying subtitles if they are not out of sync from the beginning of the video
- (*Still not decided if it will be part of repo or not) Fix wrong formated characters: � -> š, đ...

## Why use this?

If your subtitle file is slightly out of sync with your video - either too early or too late - this tool makes it quick and easy to correct that.
