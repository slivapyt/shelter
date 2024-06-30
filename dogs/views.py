from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm, inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView
from dogs.forms import DogForm, ParentForm
from dogs.models import Category, Dog, Parent


class IndexView(TemplateView):
    template_name = 'dogs/index.html'
    extra_context = {
        'title': 'Питомник - главное'
    }
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Category.objects.all()[:3]
        return context_data



class CategoryListView(ListView):
    model = Category
    extra_context = {
        'title': 'Питомник - все наши породы'
    }


class DogListView(ListView):
    model = Dog
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(category_id=self.kwargs.get('pk'))
        return queryset
    
    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        category_item = Category.objects.get(pk=self.kwargs.get('pk'))
        context_data['category_pk'] = category_item.pk,
        context_data['title'] = f'Собаки породы - все наши породы { category_item.name }'

        return context_data



class DogCreateView(CreateView):
    model = Dog
    form_class = DogForm
    success_url = reverse_lazy('dogs:categories')


class DogUpdateView(UpdateView):
    model = Dog
    form_class = DogForm
    
    def get_context_data(self, **kwargs):
        context_data =  super().get_context_data(**kwargs)
        ParentFormset = inlineformset_factory(Dog, Parent, form=ParentForm, extra=1)
        if self.request.method == 'POST':
            formset = ParentFormset(self.request.POST, instance=self.object)
        else:
            formset = ParentFormset(instance=self.object)

        context_data['formset'] = formset
        return context_data
    
    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('dogs:dog_update', args=[self.kwargs.get('pk')])

class DogDeleteView(DeleteView):
    model = Dog
    success_url = reverse_lazy('dogs:categories')