# Learning Data Collection

## Overview
The Trees of Germany app includes a privacy-focused learning analytics system that tracks user interactions during tree identification exercises. All data is stored locally in the user's browser using IndexedDB, ensuring user privacy and offline functionality.

## Implementation Details

### Storage
- Uses browser's IndexedDB API
- Database name: `TreeLearningDB` (version 1)
- Object store: `learningEvents`
- Data persists across page reloads and browser sessions
- Completely client-side (no server storage)

### Data Structure
Each learning event is stored as a JSON object with the following fields:
```json
{
  "timestamp": "2024-03-21T14:30:45.123Z",  // ISO timestamp of the event
  "selectedSpecies": "Fagus sylvatica",      // Latin name of selected species
  "availableOptions": [                      // All options shown to user
    "Fagus sylvatica",
    "Quercus robur"
  ],
  "wasCorrect": true,                        // Whether selection was correct
  "timeElapsedMs": 2500,                     // Time since page load in ms
  "imageId": 42,                             // ID of the tree image shown
  "clickNumber": 1                           // 1st or 2nd attempt
}
```

### Data Collection
Data is collected automatically during the learning process:
- Each button click in the tree identification interface triggers a new event
- Time elapsed is measured from page load to click
- Multiple attempts are tracked via `clickNumber`
- Both correct and incorrect answers are stored

### Data Export
Users can export their learning data at any time:
- Download button located in the top-right navbar
- Exports all stored events as a single JSON file
- Filename format: `tree-learning-data-YYYY-MM-DD.json`
- Data is pretty-printed (2-space indentation) for readability

## Privacy Considerations
- All data stays in the user's browser
- No server transmission of learning data
- Data persists until user clears browser data
- No personal identifiers collected

## Technical Implementation
The feature is implemented across two main components:

1. Event Logging (learn_trees.html):
```javascript
logLearningEvent(speciesId) {
    this.clickCount++;
    const timeElapsed = Date.now() - this.pageLoadTime;
    // ... store event data in IndexedDB
}
```

2. Data Export (base.html):
```javascript
async function downloadLearningData() {
    // ... retrieve and download data from IndexedDB
}
```

## Future Considerations
Potential enhancements could include:
- Data visualization dashboard
- Learning progress tracking
- Export format options (CSV, Excel)
- Data filtering capabilities
- Learning pattern analysis tools
