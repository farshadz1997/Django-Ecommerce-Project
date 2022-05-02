from .models import Category

def categories(request):
    return {'Categories': Category.objects.all()}