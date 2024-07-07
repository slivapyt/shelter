from django.urls import path
from dogs.apps import DogsConfig
from dogs.views import CategoryListView, DogListView, DogCreateView, DogUpdateView, DogDeleteView, IndexView
from django.views.decorators.cache import cache_page, never_cache # необходимый импорт для кеша
app = DogsConfig.name

urlpatterns = [
    path('', cache_page(60)(IndexView.as_view()), name='index'), #кеширование через урлы
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('<int:pk>/dogs/', DogListView.as_view(), name='category'),
    path('dogs/create', DogCreateView.as_view(), name='dog_create'),
    path('dogs/update/<int:pk>/', DogUpdateView.as_view(), name='dog_update'),
    path('dogs/delete/<int:pk>/', never_cache(DogDeleteView.as_view()), name='dog_delete'), #  урл который не будет участвовать в кеше
]
