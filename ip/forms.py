from django import forms
from django.core.validators import URLValidator


class URLShortenForm(forms.Form):
    original_url = forms.URLField(label="Enter URL to shorten", validators=[URLValidator()])