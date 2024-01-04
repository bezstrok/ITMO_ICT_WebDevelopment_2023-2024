from django.db.models import Q
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, RedirectView

from .models import Tour


class TourListView(ListView):
	model = Tour
	paginate_by = 5
	template_name = 'tours/explore.html'
	
	def get_queryset(self):
		queryset = super().get_queryset().filter(start_date__gt=timezone.localdate())
		
		search_query = self.request.GET.get('search', '')
		
		if search_query:
			queryset = queryset.filter(
				Q(name__icontains=search_query) |
				Q(country__icontains=search_query) |
				Q(description__icontains=search_query)
			)
		
		queryset = queryset.order_by('country')
		
		return queryset


class TourDetailView(RedirectView):
	url = reverse_lazy('explore')
