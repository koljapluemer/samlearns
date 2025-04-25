from django.conf import settings

class LanguagePreferenceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check for language preference in cookie (set by JavaScript)
        preferred_lang = request.COOKIES.get('preferred_lang')
        
        # If no preferred language in cookie, default to 'de'
        if not preferred_lang:
            preferred_lang = 'de'
        
        # Attach the preferred language to the request
        request.preferred_language = preferred_lang
        
        response = self.get_response(request)
        return response 