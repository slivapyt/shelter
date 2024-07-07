from django.core.cache import cache
from config import settings
from dogs.models import Category


def get_categories_cache():
	if settings.CACHE_ENABLED:  # проверка включен ли кеш в settings
		key = 'category_list'  # ключевое значение для кеша
		category_list = cache.get(key)  # получаем кеш по обозначенному ключу
		if category_list is None:  # проверяем есть ли в кеше объекты
			category_list = Category.objects.all()
			cache.set(key, category_list)  # выводим объекты по ключу из кеша
	else:
		category_list = Category.object.all()  # получаем объекты из бд
	return category_list
