from django.shortcuts import render, redirect
from .forms import URLShortenForm
from .models import ShortURL
from django.http import HttpResponse
from django.utils import timezone
from django.core.cache import cache

# Create your views here.
def shorten_url_view(request):
    if request.method == 'POST':
        form = URLShortenForm(request.POST)
        if form.is_valid():
            original_url = form.cleaned_data['original_url']
            short_url, created = ShortURL.objects.get_or_create(original_url=original_url)
            return HttpResponse(f"Shortened URL: http://localhost:8000/{short_url.short_key}")
    else:
        form = URLShortenForm()
    return render(request, 'IP/index.html', {'form': form})

def redirect_url_view(request, short_key):
    user_ip = request.META.get('REMOTE_ADDR')
    access_count_key = f"{user_ip}:{short_key}_access_count"
    access_block_key = f"{user_ip}:block"

    # Check if the IP is blocked
    if cache.get(access_block_key):
        return HttpResponse("You are temporarily blocked. Please try again.", status=403)
    
    # Increment access count
    access_count = cache.get(access_count_key, 0) + 1
    cache.set(access_count_key, access_count, timeout=60) 

    # Block IP if more than 3 accesses within 1 minute
    if access_count > 3:
        cache.set(access_block_key, True, timeout=300)  # Block IP for 5 minutes
        return HttpResponse("Too many requests. You are temporarily blocked.", status=403)

    # Redirect to the original URL if not blocked
    try:
        short_url = ShortURL.objects.get(short_key=short_key)
        return redirect(short_url.original_url)
    except ShortURL.DoesNotExist:
        return HttpResponse("Invalid URL", status=404)