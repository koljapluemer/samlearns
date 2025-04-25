# Keyboard Navigation in Tree Learning

## Overview
The tree identification game supports keyboard navigation to enhance accessibility and provide a faster interaction method for users who prefer keyboard controls.

## Implementation

### Key Bindings
- **Left Arrow (←)**: Selects the left button
- **Right Arrow (→)**: Selects the right button

### Behavior Details
- Key bindings are position-based, not content-based (i.e., left arrow always selects the physically left button)
- Keys remain active after an incorrect selection, allowing for a second attempt
- Keys are disabled after the correct answer is found (during the 1-second delay before the next question)
- Keyboard selection triggers the same events as mouse clicks:
  - Learning event logging
  - Visual feedback (greying out wrong answers)
  - Success indication (green highlight)

## Technical Implementation
The keyboard functionality is implemented in the `handleKeyPress` function:

```javascript
handleKeyPress(event) {
    if (this.foundCorrectAnswer) return;
    const buttons = Array.from(document.querySelectorAll('.species-option'));
    if (event.key === 'ArrowLeft' && buttons[0]) {
        this.handleClick(parseInt(buttons[0].getAttribute('data-species-id')));
    } else if (event.key === 'ArrowRight' && buttons[1]) {
        this.handleClick(parseInt(buttons[1].getAttribute('data-species-id')));
    }
}
```

Key features:
- Uses DOM order to determine left/right buttons
- Shares the same logic as mouse clicks via `handleClick`
- Maintains button state consistency between keyboard and mouse interaction
- Properly cleans up event listeners when component is destroyed

## User Experience
- Provides a quick, ergonomic alternative to mouse interaction
- Maintains visual feedback consistency with mouse clicks
- Allows rapid progression through learning exercises
- Supports mixed interaction (users can switch between mouse and keyboard)

## Accessibility Considerations
- Physical button layout matches arrow key directions
- Visual feedback is consistent between mouse and keyboard interaction
- Disabled states are properly maintained for both input methods
- Success/failure states are clearly indicated regardless of input method
