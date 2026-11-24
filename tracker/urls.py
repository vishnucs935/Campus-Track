import json
from django.http import JsonResponse
from django.urls import path
from django.views.decorators.http import require_http_methods, require_POST
from .models import Issue


@require_http_methods(["GET", "POST"])
def issues(request):
    if request.method == "GET":
        return JsonResponse(list(Issue.objects.order_by("-id").values()), safe=False)
    if request.content_type != "application/json":
        return JsonResponse({"error": "Use application/json."}, status=415)
    try:
        data = json.loads(request.body)
    except (ValueError, UnicodeDecodeError):
        data = None
    fields = {}
    for name, limit in (("title", 120), ("location", 100)):
        value = data.get(name) if isinstance(data, dict) else None
        if not isinstance(value, str) or not 1 <= len(value.strip()) <= limit:
            return JsonResponse({"error": f"Enter a {name} of 1 to {limit} characters."}, status=400)
        fields[name] = value.strip()
    issue = Issue.objects.create(**fields)
    return JsonResponse({"id": issue.pk, **fields, "resolved": False}, status=201)


@require_POST
def resolve(request, pk):
    if request.content_type != "application/json":
        return JsonResponse({"error": "Use application/json."}, status=415)
    if not Issue.objects.filter(pk=pk).update(resolved=True):
        return JsonResponse({"error": "Issue not found."}, status=404)
    return JsonResponse({"id": pk, "resolved": True})


urlpatterns = [path("api/issues", issues), path("api/issues/<int:pk>/resolve", resolve)]

# Serve the compiled clients alongside the API for the local demonstration.
from django.conf import settings
from django.views.static import serve
from django.urls import re_path

site = settings.BASE_DIR / "site"
urlpatterns += [
    path("", serve, {"path": "index.html", "document_root": site}),
    path("report/", serve, {"path": "report/index.html", "document_root": site}),
    re_path(r"^(?P<path>(?:assets|report)/.+)$", serve, {"document_root": site}),
]
