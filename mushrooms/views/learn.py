from django.shortcuts import render
from django.db.models import Count
from random import choice, sample
from ..models import MushroomSpecies, MushroomImage

def learn(request):
    # Get all tree species that have at least one image
    species_with_images = MushroomSpecies.objects.annotate(
        image_count=Count('mushroomimage')
    ).filter(image_count__gt=0)
    
    # Select two random species
    selected_species = sample(list(species_with_images), 2)
    
    # Randomly choose one of them as the correct answer
    correct_species = choice(selected_species)
    
    # Get a random image from the correct species
    correct_image = choice(list(correct_species.mushroomimage_set.filter(is_blacklisted=False)))
    
    # Serialize species data for JSON
    species_data = [
        {
            'id': species.id,
            'latin_name': species.latin_name,
            'german_name': species.german_name,
            'english_name': species.english_name,
        }
        for species in selected_species
    ]
    
    # Create a dict for JSON serialization but keep the full image object for template
    image_data = {'id': correct_image.id}
    
    context = {
        'correct_species': {'id': correct_species.id},  # Only need the ID for comparison
        'species_options': species_data,
        'mushroom_image': correct_image,  # Keep the full object for template rendering
    }
    
    return render(request, 'mushrooms/learn.html', context) 