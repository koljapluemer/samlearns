# Language Selection Feature

## Overview
The language selection feature allows users to switch between different language interfaces and persists their preference across sessions. The implementation uses a combination of Django backend logic and Alpine.js for frontend state management.

## Technical Implementation

### Backend Components

1. **URL Structure**
   - Root URL (`/withvideos/`) redirects to preferred language
   - Language-specific URLs follow pattern: `/withvideos/videos/<lang_code>/`
   - Language code is part of all relevant URLs

2. **Middleware**
   - `LanguagePreferenceMiddleware` checks for language preference in cookies
   - Defaults to 'de' if no preference is set
   - Attaches preferred language to request object

3. **Views**
   - Root view redirects to preferred language
   - List view sets language preference cookie
   - Language code is passed through URL parameters

### Frontend Components

1. **Alpine.js Store**
   ```javascript
   Alpine.store('language', {
       current: localStorage.getItem('preferred_lang') || 'de',
       set(lang) {
           this.current = lang;
           localStorage.setItem('preferred_lang', lang);
       }
   });
   ```

2. **Language Selector**
   - Dropdown menu using Bulma select component
   - Bound to Alpine store
   - Updates URL and localStorage on change

3. **Persistence**
   - Language preference stored in localStorage
   - Cookie set for server-side access
   - Preference persists across page reloads

## Flow

1. **Initial Visit**
   - User visits root URL
   - Middleware checks for cookie
   - Redirects to preferred language or default ('de')

2. **Language Selection**
   - User selects language from dropdown
   - Alpine store updates localStorage
   - Page redirects to new language URL
   - Server sets cookie for future visits

3. **Subsequent Visits**
   - Root URL redirects to last selected language
   - Language preference persists across sessions

## Technical Notes

- Uses Django's cookie-based session management
- Implements client-side state with Alpine.js
- Maintains URL structure for bookmarking and sharing
- Graceful fallback to German if no preference set
