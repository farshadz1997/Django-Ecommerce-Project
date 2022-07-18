from django.views.generic.base import TemplateView
from Products.models import Product, Slider


class HomePage(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_products"] = Product.products.all().order_by("-created_at")[:8]
        context["top_sellers"] = Product.products.all().order_by("-sold")[:3]
        context["slider"] = Slider.objects.all()
        if self.request.user.is_authenticated:
            context["recently_viewed"] = Product.products.filter(timestamps__user=self.request.user).order_by("-timestamps__timestamp")[:3]
        return context
