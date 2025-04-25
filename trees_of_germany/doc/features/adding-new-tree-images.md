# Adding New Tree Images

## For Users

### Directory Structure
Tree images are organized in the `static/trees/` directory, with each tree species having its own folder named after its Latin name (e.g., `Quercus robur`).

### Required Files
For each tree image, you need three files:
1. The image file itself (e.g., `quercus_robur_flickr_123456.jpg`)
2. A JSON metadata file with the same name (e.g., `quercus_robur_flickr_123456.jpg.json`)
3. A text file with the same name (e.g., `quercus_robur_flickr_123456.jpg.txt`)

### Adding New Images
1. Create a folder with the Latin name of the species if it doesn't exist
2. Place the image and its associated files in the appropriate species folder
3. Run the import command:
   ```bash
   python manage.py import_tree_images
   ```

## Technical Details

### Data Models
- `TreeSpecies`: Stores tree species information (Latin, German, and English names)
- `TreeImage`: Links images to species and stores metadata (path, credits, blacklist status)

### Image Processing
The `import_tree_images` management command:

1. **Species Discovery**
   - Scans the `static/trees/` directory
   - Creates `TreeSpecies` objects based on folder names
   - Uses folder names as Latin names (can be enhanced with proper translations)

2. **Image Processing**
   - Reads JSON metadata files for each image
   - Extracts:
     - Credit information (username, Flickr URL)
     - Tags for blacklist checking

3. **Blacklist Detection**
   - Converts all species names to lowercase without spaces
   - Checks image tags against other species names
   - Blacklists images if tags suggest wrong species identification

4. **Database Storage**
   - Creates `TreeImage` records with:
     - Relative path to image
     - Species relationship
     - Credit information
     - Blacklist status

### File Structure
```
static/trees/
└── [Latin Name]/
    ├── image_name.jpg
    ├── image_name.jpg.json
    └── image_name.jpg.txt
```

### JSON Metadata Format
```json
{
    "id": "flickr_photo_id",
    "owner": {
        "nsid": "flickr_user_id",
        "username": "photographer_name"
    },
    "tags": ["tag1", "tag2", ...],
    ...
}
```

### Error Handling
- Command is idempotent (safe to run multiple times)
- Handles missing files gracefully
- Reports errors without stopping the import process
- Uses Django's logging system for error reporting

### Future Enhancements
- Add proper translations for German and English names
- Implement image format conversion (e.g., to WebP)
- Add validation for image quality and dimensions
- Enhance blacklist detection algorithm
