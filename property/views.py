from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.utils.decorators import method_decorator

from .forms import PropertyCategoryForm, PropertyForm
from django.views.generic import CreateView, ListView, UpdateView
from .models import PropertyCategory, Property
from decorator import is_user, is_admin_or_user, is_admin


# Create your views here.

@method_decorator(is_admin(), name='dispatch')
class PropertyCategoryCreateView(SuccessMessageMixin, CreateView):
    form_class = PropertyCategoryForm
    template_name = 'property/property_category_create_update.html'
    success_url = '/property/category/list/'
    success_message = 'Property Message Created Successfully'


@method_decorator(is_admin(), name='dispatch')
class PropertyCategoryListView(ListView):
    model = PropertyCategory
    context_object_name = 'property_category'
    template_name = 'property/property_category_list_view.html'


@method_decorator(is_admin(), name='dispatch')
class PropertyCategoryUpdateView(SuccessMessageMixin, UpdateView):
    form_class = PropertyCategoryForm
    model = PropertyCategory
    template_name = 'property/property_category_create_update.html'
    success_url = '/property/category/list/'
    success_message = 'Property Category Updated Successfully'


@method_decorator(is_admin_or_user(), name='dispatch')
class PropertyCreateView(SuccessMessageMixin, CreateView):
    form_class = PropertyForm
    template_name = 'property/property_create_update_view.html'
    success_message = 'Property Created Successfully'
    success_url = '/dashboard/my/properties/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


@method_decorator(is_admin(), name='dispatch')
class PropertyListView(ListView):
    model = Property
    context_object_name = 'properties'
    template_name = 'property/property_list_view.html'


@method_decorator(is_admin_or_user(), name='dispatch')
class PropertyUpdateView(SuccessMessageMixin, UpdateView):
    form_class = PropertyForm
    model = Property
    template_name = 'property/property_create_update_view.html'
    success_message = 'Property Created Successfully'
    success_url = '/dashboard/my/properties/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
