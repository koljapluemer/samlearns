from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from guest_user.decorators import allow_guest_user
import string
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from triangles.models import ClozeTemplate, Topic, TopicProgress, ClozeTemplateGapProgress, LearningEvent, Distractor
from triangles.utils import get_due_topic, get_due_gap_index_for_cloze_template, get_random_relevant_distractor








