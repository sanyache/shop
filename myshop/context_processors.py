from .models import Category

def getting_categories(request):
    categories = Category.objects.all()
    return locals()