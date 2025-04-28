# Sam Learns

A Django-based learning platform.

## Local Development

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with the following variables:
```
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
YOUTUBE_API_KEY=your-youtube-api-key
OPENAI_API_KEY=your-openai-api-key
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

## Heroku Deployment

1. Install the Heroku CLI and login:
```bash
heroku login
```

2. Create a new Heroku app:
```bash
heroku create your-app-name
```

3. Set up environment variables on Heroku:
```bash
heroku config:set DJANGO_SECRET_KEY=your-secret-key
heroku config:set DJANGO_DEBUG=False
heroku config:set DJANGO_ALLOWED_HOSTS=your-app-name.herokuapp.com
heroku config:set YOUTUBE_API_KEY=your-youtube-api-key
heroku config:set OPENAI_API_KEY=your-openai-api-key
```

4. Add the Heroku remote:
```bash
heroku git:remote -a your-app-name
```

5. Deploy to Heroku:
```bash
git push heroku main
```

6. Run migrations on Heroku:
```bash
heroku run python manage.py migrate
```

7. Create a superuser on Heroku:
```bash
heroku run python manage.py createsuperuser
```

## Environment Variables

- `DJANGO_SECRET_KEY`: Django secret key for security
- `DJANGO_DEBUG`: Set to False in production
- `DJANGO_ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `YOUTUBE_API_KEY`: YouTube API key for video functionality
- `OPENAI_API_KEY`: OpenAI API key for AI features

## Stack

- Django, app-based
- using Bulma for style

## Projects

### Trees of Germany

![screenshot mockup](/trees_of_germany/doc/img/screen1.png)

[Documentation](/trees_of_germany/README.md)