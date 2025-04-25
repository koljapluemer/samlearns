# Trees of Germany

A Django application for managing and displaying tree species found in Germany.

## Management Commands

### Importing Tree Images

To import tree images and their metadata into the database:

```bash
python manage.py import_tree_images
```

This command will:
- Create TreeSpecies objects based on folder names in `static/trees/`
- Import image metadata and credit information from JSON files
- Set up proper relationships between species and their images
- Automatically blacklist images that might show the wrong species based on their tags

The command is idempotent and can be safely run multiple times without creating duplicates.
