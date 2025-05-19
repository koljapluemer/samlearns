from django.db import models

# Create your models here.
class MushroomSpecies(models.Model):
    latin_name = models.CharField(max_length=255)
    german_name = models.CharField(max_length=255)
    english_name = models.CharField(max_length=255)

    def __str__(self):
        return self.latin_name

class MushroomImage(models.Model):
    path = models.CharField(max_length=255)
    mushroom_species = models.ForeignKey(MushroomSpecies, on_delete=models.CASCADE)
    is_blacklisted = models.BooleanField(default=False)

    credit_user_name = models.CharField(max_length=255, null=True, blank=True)
    credit_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.mushroom_species.latin_name} - {self.path}"

    def get_usable_url(self):
        if self.is_blacklisted:
            return None
        # The path is already the full URL path, just prepend the domain
        return f"https://samlearns.com{self.path}"
