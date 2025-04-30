from django.db import models
from django.conf import settings
from django.core.files.storage import default_storage
from django.templatetags.static import static
# Create your models here.
class TreeSpecies(models.Model):
    latin_name = models.CharField(max_length=255)
    german_name = models.CharField(max_length=255)
    english_name = models.CharField(max_length=255)

    def __str__(self):
        return self.latin_name

class TreeImage(models.Model):
    path = models.CharField(max_length=255)
    tree_species = models.ForeignKey(TreeSpecies, on_delete=models.CASCADE)
    is_blacklisted = models.BooleanField(default=False)

    credit_user_name = models.CharField(max_length=255, null=True, blank=True)
    credit_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.tree_species.latin_name} - {self.path}"

    def get_usable_url(self):
        if self.is_blacklisted:
            return None
        # Use the storage backend to get the proper URL
        return default_storage.url(self.path)
