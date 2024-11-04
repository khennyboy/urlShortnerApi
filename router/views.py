from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import Route
from .forms import RouterForm
from django.views.generic import ListView
import json
from django.http import JsonResponse
from .parse_url import normalize_url

def home(request):
    form = RouterForm(request.POST or None)

    if request.method == 'POST':
        is_ajax = request.headers.get('x-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            try:
                data = json.loads(request.body)
                url = data.get("original_url", "").strip()

                if not url:
                    return JsonResponse({"error": "Empty field"}, status=400)
                normalized_url = normalize_url(url)
                existing_url = Route.objects.filter(original_url=normalized_url).first()
                
                if existing_url:
                    shorten_url = request.build_absolute_uri(existing_url.get_absolute_url())
                    return JsonResponse({
                        "message": "URL already exists",
                        "shorten_url": shorten_url
                    }, status=200)

                form = RouterForm(data={'original_url': normalized_url})
                
                if form.is_valid():
                    saved_url = form.save()
                    shorten_url = request.build_absolute_uri(saved_url.get_absolute_url())
                    
                    shorten_data = {
                        "original_url": saved_url.original_url,
                        "shorten_url": shorten_url
                    }

                    return JsonResponse({
                        "success": "The URL was successfully shortened",
                        "data": shorten_data
                    }, status=200 )
                
                return JsonResponse({"errors": form.errors}, status=400)

            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON data"}, status=400)

        else:
            if form.is_valid():
                form.save()
                messages.success(request, "URL has been successfully shortened")
                return redirect('home')

    return render(request, 'router/home.html', {"form": form})



def how_to(request):
    # return HttpResponse("<h1>About Page</h1>")
    return render(request, 'router/how_to_use.html')

class URLListView(ListView):
    model = Route
    context_object_name = 'urls'
    paginate_by = 10

def redirector(request, key):

    instance = get_object_or_404(Route, key= key)
    return redirect(instance.original_url)