from django.urls import path
from cms.views.german_with_videos.pages import cms_home, actions
from cms.views.german_with_videos.import_channel_videos import import_channel_videos
from cms.views.german_with_videos.import_playlist_videos import import_playlist_videos
from cms.views.german_with_videos.bulk_import_videos import bulk_import_videos
from cms.views.german_with_videos.review_videos import review_videos
from cms.views.german_with_videos.update_video_statuses import update_video_statuses
from cms.views.german_with_videos.list_all_videos import list_all_videos
from cms.views.german_with_videos.video_details import video_details
from cms.views.german_with_videos.update_video_status import update_video_status
from cms.views.german_with_videos.generate_snippets import generate_snippets
from cms.views.german_with_videos.generate_translations import generate_translations
from cms.views.german_with_videos.publish_video import publish_video
from cms.views.german_with_videos.reset_snippets import reset_snippets
from cms.views.german_with_videos.export_snippets_csv import export_snippets_csv
from cms.views.german_with_videos.mark_videos_without_german_subtitles import mark_videos_without_german_subtitles
from cms.views.german_with_videos.generate_snippets_for_all_shortlisted import generate_snippets_for_all_shortlisted
from cms.views.german_with_videos.generate_translations_for_all_snippets import generate_translations_for_all_snippets
from cms.views.german_with_videos.bulk_check_subtitles import bulk_check_subtitles
from cms.views.german_with_videos.blacklist_video import blacklist_video
from cms.views.german_with_videos.update_video_priorities import update_video_priorities
from cms.views.german_with_videos.reduce_review_priorities import reduce_review_priorities
from cms.views.german_with_videos.search_videos import search_videos
from cms.views.german_with_videos.enrich_video_metadata import enrich_video_metadata
from cms.views.german_with_videos.publish_videos_with_many_snippets import publish_videos_with_many_snippets
from cms.views.german_with_videos.manage_tags import manage_tags, remove_tag, add_tag, tag_autocomplete

app_name = 'cms'

urlpatterns = [
    path('', cms_home, name='cms_home'),
    path('actions/', actions, name='actions'),
    path('import/', import_channel_videos, name='import_channel_videos'),
    path('import-playlist/', import_playlist_videos, name='import_playlist_videos'),
    path('bulk-import/', bulk_import_videos, name='bulk_import_videos'),
    path('review/', review_videos, name='review_videos'),
    path('update-statuses/', update_video_statuses, name='update_video_statuses'),
    path('videos/', list_all_videos, name='list_all_videos'),
    path('videos/<str:youtube_id>/', video_details, name='video_details'),
    path('videos/<str:youtube_id>/update-status/', update_video_status, name='update_video_status'),
    path('videos/<str:youtube_id>/generate-snippets/', generate_snippets, name='generate_snippets'),
    path('videos/<str:youtube_id>/generate-translations/', generate_translations, name='generate_translations'),
    path('videos/<str:youtube_id>/publish/', publish_video, name='publish_video'),
    path('videos/<str:youtube_id>/reset-snippets/', reset_snippets, name='reset_snippets'),
    path('videos/<str:youtube_id>/export-snippets/', export_snippets_csv, name='export_snippets_csv'),
    path('mark-videos-without-german-subtitles/', mark_videos_without_german_subtitles, name='mark_videos_without_german_subtitles'),
    path('generate-snippets-all/', generate_snippets_for_all_shortlisted, name='generate_snippets_all'),
    path('generate-translations-all/', generate_translations_for_all_snippets, name='generate_translations_all'),
    path('bulk-check-subtitles/', bulk_check_subtitles, name='bulk_check_subtitles'),
    path('video/<str:youtube_id>/blacklist/', blacklist_video, name='blacklist_video'),
    path('update-priorities/', update_video_priorities, name='update_video_priorities'),
    path('reduce-review-priorities/', reduce_review_priorities, name='reduce_review_priorities'),
    path('search/', search_videos, name='search_videos'),
    path('enrich-metadata/', enrich_video_metadata, name='enrich_video_metadata'),
    path('publish-many-snippets/', publish_videos_with_many_snippets, name='publish_videos_with_many_snippets'),
    path('tags/', manage_tags, name='manage_tags'),
    path('tags/<int:tag_id>/', manage_tags, name='edit_tag'),
    path('videos/<str:youtube_id>/remove-tag/<int:tag_id>/', remove_tag, name='remove_tag'),
    path('videos/<str:youtube_id>/add-tag/', add_tag, name='add_tag'),
    path('tags/autocomplete/', tag_autocomplete, name='tag_autocomplete'),
]
