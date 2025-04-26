# URL Management

## Concept

The app uses a split URL system that cleanly separates public and administrative concerns:

- Public URLs (`/`) are for end-users
- CMS URLs (`/cms/`) are for content management
- Each section has its own namespace to prevent conflicts

## Implementation

URLs are split across three files:

1. `urls/__init__.py`: The main router
   - Includes both public and CMS URLs
   - Defines the base path structure

2. `urls/app.py`: Public section
   - Namespace: `uke_fingerpicking`
   - Contains all user-facing views
   - No authentication required

3. `urls/cms.py`: Admin section
   - Namespace: `uke_fingerpicking_cms`
   - Requires superuser permissions
   - Contains all management views

## Key Points

- Namespaces prevent URL name collisions
- CMS section is protected by superuser check
- Clear separation of concerns in URL structure
- Easy to add new views to either section

## Structure

The app uses a split URL system with separate namespaces for public and CMS views:

```
uke-fingerpicking/              # App root (namespace: uke_fingerpicking)
├── /                          # Public tab sheet list
└── cms/                       # CMS section (namespace: uke_fingerpicking_cms)
    ├── tabs/                  # Tab sheet management
    ├── tabs/add/             # Create new tab sheet
    └── tabs/<pk>/edit/       # Edit existing tab sheet
```

## URL Names

### Public URLs
- `tab_sheet_list`: List all tab sheets

### CMS URLs
- `tab_sheet_list`: List all tab sheets (management view)
- `tab_sheet_add`: Create new tab sheet
- `tab_sheet_edit`: Edit existing tab sheet

## Usage in Templates

```html
<!-- Public URLs -->
{% url 'uke_fingerpicking:tab_sheet_list' %}

<!-- CMS URLs -->
{% url 'uke_fingerpicking_cms:tab_sheet_list' %}
{% url 'uke_fingerpicking_cms:tab_sheet_add' %}
{% url 'uke_fingerpicking_cms:tab_sheet_edit' tab_sheet.pk %}
```
