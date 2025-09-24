# Neon Sentinel Lock Screen

A lightweight web experience that turns your futuristic artwork into an animated
lock-screen style video. Drop the provided figure into the `assets` folder,
press **Export 6s Video**, and you'll receive a WebM clip ready to convert into
an iOS Live Photo, Android lock screen video, or Windows wallpaper.

## Quick start

1. Copy your artwork into `assets/lock-subject.png`. The supplied example image
   works best as a 9:16 PNG around 1170×2532px.
2. Serve the project locally (any static server will do). For example:
   ```bash
   npx serve .
   ```
3. Open the page in Chrome or Edge.
4. Click **Replay Animation** to preview and **Export 6s Video** to download a
   looped clip.

> **Tip for iPhone lock screens:** Convert the exported `neon-lock-screen.webm`
> to a `.mov` or Live Photo (QuickTime, Kapwing, or `ffmpeg`) and set it as your
> lock screen from Photos.

## Customisation ideas

- Edit the animation colours inside `styles.css` or tweak the neon/glitch
  effects in `scripts/app.js`.
- Adjust the recording duration or resolution by changing the `canvas` size or
  the timeout inside `recordClip`.

## Requirements

- Modern Chromium-based browser (MediaRecorder + canvas capture support).
- Static file server (or open `index.html` directly for previewing only).
