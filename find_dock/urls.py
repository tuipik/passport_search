from django.urls import path

from find_dock.views import SearchResultsView, HomePageView

urlpatterns = [
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('', HomePageView.as_view(), name='home'),
]
