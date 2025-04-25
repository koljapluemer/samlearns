# Template Inheritance Structure

## Template Chain

```
base.html (project level)
    ↑
base.html (app level)
    ↑
home.html (page level)
```

## Implementation

### Project Level (`samlearns/templates/base.html`)
- Basic HTML structure
- Bulma CSS framework
- Common blocks:
  - `title`: Page title
  - `extra_css`: Additional CSS
  - `body`: Main wrapper
  - `content`: Page content
  - `extra_js`: Additional JS

### App Level (`trees_of_germany/templates/trees_of_germany/base.html`)
- Extends project base
- App navigation
- App-specific layout
- Custom `nav` block

### Page Level (`trees_of_germany/templates/trees_of_germany/home.html`)
- Extends app base
- Page-specific content
- Overrides `title` and `content`

## Django Settings

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Project templates
        'APP_DIRS': True,  # App templates
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

## Template Resolution Order
1. Project-level templates (`DIRS`)
2. App-level templates (`APP_DIRS`)

## Template Files

### 1. Project Level (`samlearns/templates/base.html`)

The root template that defines the basic HTML structure and common resources.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Sam Learns{% endblock %}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@latest/css/bulma.min.css">
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% block body %}
    <div class="container">
        {% block content %}{% endblock %}
    </div>
    {% endblock %}

    {% block extra_js %}{% endblock %}
</body>
</html>
```

#### Key Features:
- Loads Bulma CSS framework
- Defines basic HTML structure
- Provides template blocks for customization:
  - `title`: Page title
  - `extra_css`: Additional CSS files
  - `body`: Main content wrapper
  - `content`: Page-specific content
  - `extra_js`: Additional JavaScript files

### 2. App Level (`trees_of_germany/templates/trees_of_germany/base.html`)

The app-specific base template that extends the project template.

```html
{% extends "base.html" %}

{% block body %}
    {% block nav %}
    <nav class="navbar is-primary" role="navigation" aria-label="main navigation">
        <div class="navbar-brand">
            <a class="navbar-item" href="{% url 'trees_of_germany:home' %}">
                Trees of Germany
            </a>
        </div>
    </nav>
    {% endblock %}

    <div class="container">
        {% block content %}{% endblock %}
    </div>
{% endblock %}
```

#### Key Features:
- Extends project-level base template
- Adds app-specific navigation
- Provides app-specific layout structure
- Defines `nav` block for navigation customization

### 3. Page Level (`trees_of_germany/templates/trees_of_germany/home.html`)

Individual page templates that extend the app-level template.

```html
{% extends "trees_of_germany/base.html" %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
    <section class="hero is-primary is-fullheight">
        <div class="hero-body">
            <div class="container has-text-centered">
                <h1 class="title is-1">
                    {{ title }}
                </h1>
                <h2 class="subtitle">
                    Discover the beautiful flora of Germany
                </h2>
            </div>
        </div>
    </section>
{% endblock %}
```

#### Key Features:
- Extends app-level base template
- Focuses only on page-specific content
- Customizes title and content blocks

## Usage Guidelines

### Creating New Pages

1. Create a new template in `trees_of_germany/templates/trees_of_germany/`
2. Extend the app-level base template:
   ```html
   {% extends "trees_of_germany/base.html" %}
   ```
3. Override necessary blocks:
   - `title`: Page title
   - `content`: Main content
   - `nav`: Navigation (if different from default)

### Adding App-Specific Features

1. Modify `trees_of_germany/templates/trees_of_germany/base.html`
2. Add new blocks as needed
3. Update existing blocks to include app-specific elements

### Adding Project-Wide Features

1. Modify `samlearns/templates/base.html`
2. Add new blocks for project-wide customization
3. Update existing blocks to include common elements

## Technical Implementation

### Django Settings

The template inheritance is enabled by configuring the `TEMPLATES` setting in `settings.py`:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Project-level templates
        'APP_DIRS': True,  # App-level templates
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

### Template Resolution

Django's template loader follows this order:
1. Project-level templates (`DIRS`)
2. App-level templates (`APP_DIRS`)
