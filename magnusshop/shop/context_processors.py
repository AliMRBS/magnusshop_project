from .models import Category

def category_context(request):
    categories = Category.objects.filter(parent=None).prefetch_related('children')
    return {'categories': categories}
