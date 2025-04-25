import os
import json
from django.core.management.base import BaseCommand
from trees_of_germany.models import TreeSpecies, TreeImage
from django.conf import settings

class Command(BaseCommand):
    help = 'Import tree species and images from the static directory'

    def get_species_from_folders(self):
        """Get all tree species from the folder names."""
        static_path = os.path.join(settings.BASE_DIR, 'trees_of_germany', 'static', 'trees')
        return [name for name in os.listdir(static_path) 
                if os.path.isdir(os.path.join(static_path, name))]

    def create_tree_species(self):
        """Create TreeSpecies objects for each folder."""
        species_folders = self.get_species_from_folders()
        species_objects = {}
        
        for species_name in species_folders:
            # For now, we'll use the latin name for all fields
            # In a real application, you might want to add proper translations
            species, created = TreeSpecies.objects.get_or_create(
                latin_name=species_name,
                defaults={
                    'german_name': species_name,
                    'english_name': species_name,
                }
            )
            species_objects[species_name] = species
            if created:
                self.stdout.write(f'Created species: {species_name}')
        
        return species_objects

    def should_blacklist(self, tags, all_species_names):
        """Check if the image should be blacklisted based on tags."""
        # Convert species names to lowercase without spaces for comparison
        species_identifiers = {name.lower().replace(' ', '') for name in all_species_names}
        
        for tag in tags:
            # Skip the tag that corresponds to the current species
            if tag in species_identifiers:
                species_identifiers.remove(tag)
                continue
            
            # If any remaining species identifier is found in tags, blacklist the image
            if tag in species_identifiers:
                return True
        return False

    def handle(self, *args, **options):
        # Create species objects
        species_objects = self.create_tree_species()
        all_species_names = list(species_objects.keys())
        static_path = os.path.join(settings.BASE_DIR, 'trees_of_germany', 'static', 'trees')

        # Process each species folder
        for species_name, species_obj in species_objects.items():
            species_path = os.path.join(static_path, species_name)
            
            # Get all JSON files in the species directory
            for filename in os.listdir(species_path):
                if not filename.endswith('.json'):
                    continue

                json_path = os.path.join(species_path, filename)
                image_path = filename[:-5]  # Remove .json extension

                try:
                    with open(json_path, 'r') as f:
                        metadata = json.load(f)

                    # Extract credit information
                    credit_user_name = metadata['owner']['username']
                    credit_url = f"https://www.flickr.com/photos/{metadata['owner']['nsid']}/{metadata['id']}"

                    # Check if image should be blacklisted
                    tags = [tag.lower() for tag in metadata.get('tags', [])]
                    is_blacklisted = self.should_blacklist(tags, all_species_names)

                    # Create or update TreeImage
                    relative_path = os.path.join('trees', species_name, image_path)
                    tree_image, created = TreeImage.objects.get_or_create(
                        path=relative_path,
                        tree_species=species_obj,
                        defaults={
                            'credit_user_name': credit_user_name,
                            'credit_url': credit_url,
                            'is_blacklisted': is_blacklisted,
                        }
                    )

                    status = 'Created' if created else 'Updated'
                    self.stdout.write(f'{status} image: {relative_path}')

                except Exception as e:
                    self.stderr.write(f'Error processing {json_path}: {str(e)}')

        self.stdout.write(self.style.SUCCESS('Successfully imported tree species and images')) 