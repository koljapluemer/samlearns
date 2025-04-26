# Stats Tracking

This app tracks user progress for each beat played during tab practice. Progress is logged locally in the browser using IndexedDB for robust, structured storage.

## What is Tracked
- Timestamp of each beat
- Song title and artist
- Song iteration (run count)
- Beat index and total beats
- Expected note and played note
- State (correct/incorrect/missed)
- Timing distance to perfect middle (ms)
- Timing category (very early, early, perfect, etc.)
- BPM

## IndexedDB Schema
- **Database:** `uke_progress_db`
- **Object Store:** `uke_progress`
- **Key:** `id` (auto-incremented)
- **Fields:**
  - `timestamp`: number (ms since epoch)
  - `songTitle`: string
  - `songArtist`: string
  - `runCount`: number (iteration of the song)
  - `beatIdx`: number (index of the beat)
  - `beatsTotal`: number (total beats in the song)
  - `expectedNote`: string
  - `playedNote`: string or null
  - `state`: string ('correct', 'incorrect', 'missed')
  - `timingDistance`: number or null (ms from perfect middle)
  - `timingCategory`: string or null (e.g. 'very-early', 'perfect', etc.)
  - `bpm`: number

Each record represents a single beat attempt and is appended as the user practices.
