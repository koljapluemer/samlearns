from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.staticfiles import finders
from storages.backends.s3boto3 import S3Boto3Storage
import os
import environ

class Command(BaseCommand):
    help = 'Upload static files to R2'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be uploaded without uploading'
        )

    def handle(self, *args, **options):
        # Initialize environ
        env = environ.Env()
        env.read_env(os.path.join(settings.BASE_DIR, '.env'))
        
        # Debug output
        self.stdout.write(f"R2 Account ID: {env('R2_ACCOUNT_ID')}")
        self.stdout.write(f"R2 Bucket Name: {env('R2_BUCKET_NAME')}")
        self.stdout.write(f"R2 Endpoint URL: {settings.AWS_S3_ENDPOINT_URL}")
        
        dry_run = options['dry_run']
        
        # Initialize R2 storage with proper configuration
        storage = S3Boto3Storage(
            access_key=env('R2_ACCESS_KEY_ID'),
            secret_key=env('R2_SECRET_ACCESS_KEY'),
            bucket_name=env('R2_BUCKET_NAME'),
            endpoint_url=f"https://{env('R2_ACCOUNT_ID')}.r2.cloudflarestorage.com",
            custom_domain=f"{env('R2_BUCKET_NAME')}.r2.dev",
            default_acl='public-read',
            object_parameters={'CacheControl': 'max-age=86400'}
        )
        
        # Find all static files
        for finder in finders.get_finders():
            for path, storage_instance in finder.list([]):
                # Get the full path and the relative path for the file
                absolute_path = storage_instance.path(path)
                
                if dry_run:
                    self.stdout.write(f'Would upload: {path}')
                else:
                    # Open and upload the file
                    with open(absolute_path, 'rb') as f:
                        storage.save(path, f)
                    self.stdout.write(
                        self.style.SUCCESS(f'Uploaded: {path}')
                    )
        
        if dry_run:
            self.stdout.write(self.style.SUCCESS('\nDry run complete - no files were uploaded'))
        else:
            self.stdout.write(self.style.SUCCESS('\nAll static files uploaded to R2')) 