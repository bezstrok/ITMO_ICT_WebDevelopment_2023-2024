from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.views import LogoutView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View

User = get_user_model()


class LogoutView(LogoutView):
	next_page = reverse_lazy('home')


class RegisterView(View):
	def post(self, request, *args, **kwargs):
		email = request.POST.get('email')
		password = request.POST.get('password')
		confirm_password = request.POST.get('confirm_password')
		
		if User.objects.filter(email=email).exists():
			return JsonResponse({'error': 'Email already in use'}, status=400)
		
		if password != confirm_password:
			return JsonResponse({'error': 'Passwords do not match'}, status=400)
		
		User.objects.create_user(email=email, password=password)
		
		return JsonResponse({'success': True})


class LoginView(View):
	def post(self, request, *args, **kwargs):
		email = request.POST.get('email')
		password = request.POST.get('password')
		user = authenticate(request, username=email, password=password)
		
		if user is not None:
			if user.is_active:
				login(request, user)
				return JsonResponse({'success': True})
			else:
				return JsonResponse({'error': 'Account is disabled'}, status=403)
		else:
			return JsonResponse({'error': 'Invalid credentials'}, status=400)
