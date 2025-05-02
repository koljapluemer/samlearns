from django.shortcuts import render, redirect
from django.conf import settings
from googleapiclient.discovery import build
from german_with_videos.models import Video, VideoStatus, Snippet, Word, Meaning, Tag, TagType
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from youtube_transcript_api import YouTubeTranscriptApi
from django.contrib import messages
from openai import OpenAI, beta
from pydantic import BaseModel
from typing import List
import re
import csv
from django.contrib.admin.views.decorators import staff_member_required
from django.db import models
from django.urls import reverse
from django.db.models import Q
from django.views.decorators.cache import cache_page, never_cache

