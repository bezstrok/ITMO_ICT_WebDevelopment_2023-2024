from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


class CreateObjectMixin:
    form_class = None
    model = None
    related_name = None
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        pk = kwargs.get('pk')
        related_object = get_object_or_404(self.model, pk=pk)
        
        if form.is_valid():
            obj = form.save(commit=False)
            setattr(obj, self.related_name, related_object)
            obj.user = request.user
            
            try:
                obj.full_clean()
                obj.save()
                return JsonResponse({'success': True})
            except ValidationError as e:
                error_message = e.messages[0]
                return JsonResponse({'error': error_message}, status=400)
        
        error_message = handlers.handle_form_errors(form)
        return JsonResponse({'error': error_message}, status=400)
