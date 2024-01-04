from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, ListView

from . import forms, mixins, models


class TourListView(ListView):
	model = models.Tour
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


class TourDetailView(DetailView):
	model = models.Tour
	template_name = 'tours/tour_detail.html'


class AddReviewView(LoginRequiredMixin, mixins.CreateObjectMixin, View):
	form_class = forms.ReviewForm
	model = models.Tour
	related_name = 'tour'


class AddBookingView(LoginRequiredMixin, mixins.CreateObjectMixin, View):
	form_class = forms.BookingForm
	model = models.Tour
	related_name = 'tour'
