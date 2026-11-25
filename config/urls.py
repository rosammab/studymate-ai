from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/", include("users.urls")),
    path("api/notes/", include("notes.urls")),
    path("api/flashcards/", include("flashcards.urls")),
    path("api/quizzes/", include("quizzes.urls")),
    path("api/documents/", include("documents.urls")),
    path("api/study-planner/", include("study_planner.urls")),
    path("api/progress/", include("progress.urls")),
    path("api/notifications/",include("notifications.urls")),
    path("api/dashboard/",include("dashboard.urls")),
    path("api/search/", include("search_engine.urls")),
    path("api/ai-assistant/", include("ai_assistant.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

    