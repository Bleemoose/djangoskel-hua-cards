from django import template
from django.template.loader import render_to_string
from django.shortcuts import reverse, get_object_or_404
from accounts.models import *

register = template.Library()
