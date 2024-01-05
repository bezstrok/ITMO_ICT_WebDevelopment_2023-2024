from django.utils import timezone
from django.views.generic import TemplateView

from tours import models


class IndexView(TemplateView):
    template_name = 'common/index.html'
    tours_on_page: int = 6
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recommended_tours'] = models.Tour.objects \
                                           .filter(start_date__gte=timezone.localdate()) \
                                           .order_by('start_date')[:self.tours_on_page]
        return context
