import os
import json
from django.core.management.base import BaseCommand
from trees_of_germany.models import TreeSpecies, TreeImage
from django.conf import settings

class Command(BaseCommand):
    help = 'Import tree species and images from the static directory'

    def get_species_from_trees_txt(self):
        """Get all tree species from trees.txt file."""
        trees_file_path = os.path.join(settings.BASE_DIR, 'trees_of_germany', 'static', 'trees', 'trees.txt')
        species_info = {}
        
        try:
            with open(trees_file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    latin_name, english_name, german_name = [name.strip() for name in line.split(',')]
                    species_info[latin_name] = {
                        'latin_name': latin_name,
                        'english_name': english_name,
                        'german_name': german_name
                    }
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading trees.txt: {str(e)}'))
            raise
        
        return species_info

    def create_tree_species(self):
        """Create TreeSpecies objects for each species in trees.txt."""
        species_info = self.get_species_from_trees_txt()
        species_objects = {}
        
        for latin_name, info in species_info.items():
            species, created = TreeSpecies.objects.get_or_create(
                latin_name=latin_name,
                defaults={
                    'german_name': info['german_name'],
                    'english_name': info['english_name'],
                }
            )
            species_objects[latin_name] = species
            if created:
                self.stdout.write(f'Created species: {latin_name} ({info["english_name"]})')
        
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
            
            # Get all files in the species directory
            try:
                files = set(os.listdir(species_path))
            except Exception as e:
                print(f"Error accessing directory {species_path}: {str(e)}")
                continue

            # Process JSON files and verify matching image files exist
            for filename in files:
                if not filename.endswith('.json'):
                    continue

                json_path = os.path.join(species_path, filename)
                
                # Handle both cases: regular .json and .jpg.json
                if filename.endswith('.jpg.json'):
                    base_image_name = filename[:-9]  # Remove .jpg.json extension
                else:
                    base_image_name = filename[:-5]  # Remove .json extension
                
                # Check if corresponding image file exists (try common image extensions)
                image_exists = False
                # Prioritize webp since that's the new format
                for ext in ['.webp', '.jpg', '.jpeg', '.png']:
                    if base_image_name + ext in files:
                        image_exists = True
                        image_path = base_image_name + ext
                        break

                if not image_exists:
                    print(f"Error: No matching image file found for {json_path}")
                    continue

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
                    print(f"Error processing {json_path}: {str(e)}")
                    continue

        self.stdout.write(self.style.SUCCESS('Successfully imported tree species and images')) 