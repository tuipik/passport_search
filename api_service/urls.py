from django.urls import path

from .views import SearchDocumentView

app_name = "api_service"

urlpatterns = [
    path("find_documents/", SearchDocumentView.as_view()),
]
