from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, ListView

from common import handlers
from . import forms, models


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


class AddReviewView(LoginRequiredMixin, View):
	form_class = forms.ReviewForm
	
	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		
		pk = kwargs.get('pk')
		tour = get_object_or_404(models.Tour, pk=pk)
		
		if form.is_valid():
			review = form.save(commit=False)
			review.tour = tour
			review.user = request.user
			review.save()
			return JsonResponse({'success': True})
		
		error_message = handlers.handle_form_errors(form)
		
		return JsonResponse({'error': error_message}, status=400)
