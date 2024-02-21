from django.http import Http404
from django.shortcuts import redirect, render
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import DriverUserCreationForm
from .models import Car, Driver


def driver_detail(request, id_driver):
	try:
		driver = Driver.objects.get(pk=id_driver)
	except Driver.DoesNotExist:
		raise Http404("Driver does not exist")
	
	return render(request, 'driver.html', {'driver': driver})


def all_drivers(request):
	drivers = Driver.objects.all()
	return render(request, 'all_drivers.html', {'drivers': drivers})


# def driver_create(request):
# 	context = {}
# 	form = DriverForm(request.POST or None)
#
# 	if form.is_valid():
# 		form.save()
#
# 	context['form'] = form
# 	return render(request, "driver_create.html", context)


def driver_register(request):
	context = {}
	form = DriverUserCreationForm(request.POST or None)
	
	if form.is_valid():
		form.save()
		return redirect('/drivers/')
	
	context['form'] = form
	return render(request, 'driver_create.html', context)


class CarListView(ListView):
	model = Car
	template_name = 'all_cars.html'


class CarDetailView(DetailView):
	model = Car
	template_name = 'car.html'


class CarUpdateView(UpdateView):
	model = Car
	fields = ['state_number', 'brand', 'model', 'color']
	template_name = 'car_create.html'
	success_url = '/cars/'


class CarDeleteView(DeleteView):
	model = Car
	success_url = '/cars/'
	template_name = 'car_delete.html'


class CarCreateView(CreateView):
	model = Car
	template_name = 'car_create.html'
	fields = ['state_number', 'brand', 'model', 'color']
	success_url = '/cars/'
