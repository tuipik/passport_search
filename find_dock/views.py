from django.db.models import Q
from django.views.generic import TemplateView, ListView

from core.models import LostPassport


class HomePageView(TemplateView):
    template_name = "home.html"


class SearchResultsView(ListView):
    model = LostPassport
    template_name = "search_results.html"
    paginate_by = 20

    def get_queryset(self):
        series_query = self.request.GET.get("series")
        number_query = self.request.GET.get("number")
        object_list = LostPassport.objects.filter(
            Q(document_series__icontains=series_query)
        ).filter(Q(document_number__icontains=number_query))
        return object_list
