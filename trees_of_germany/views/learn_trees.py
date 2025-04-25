from django.shortcuts import render
from django.db.models import Count
from random import choice, sample
from ..models import TreeSpecies, TreeImage

def learn_trees(request):
    # Get all tree species that have at least one image
    species_with_images = TreeSpecies.objects.annotate(
        image_count=Count('treeimage')
    ).filter(image_count__gt=0)
    
    # Select two random species
    selected_species = sample(list(species_with_images), 2)
    
    # Randomly choose one of them as the correct answer
    correct_species = choice(selected_species)
    
    # Get a random image from the correct species
    correct_image = choice(list(correct_species.treeimage_set.filter(is_blacklisted=False)))
    
    context = {
        'correct_species': correct_species,
        'species_options': selected_species,
        'tree_image': correct_image,
    }
    
    return render(request, 'trees_of_germany/learn_trees.html', context) 