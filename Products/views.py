from django.db.models import Q
from django.utils.timezone import now
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Category, Product, UserProductTimestamp, Brand


class ProductListView(ListView):
    queryset = Product.products.all()
    ordering = ["-in_stock", "-created_at"]
    template_name = "Products/Product_list.html"
    context_object_name = "products"
    paginate_by = 12
    extra_context = {"banner_title": "All Products"}
    

class ProductDetailView(DetailView):
    model = Product
    template_name = "Products/Product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_products"] = Product.products.all().order_by("-created_at")[:4]
        context["related_products"] = Product.products.filter(category=self.object.category, brand=self.object.brand, in_stock=True).exclude(pk=self.object.pk)[:4]
        context["banner_title"] = self.object.title
        return context
    
    def get(self, request, *args, **kwargs):
        self.user_viewed(now())
        return super().get(request, *args, **kwargs)
        
    def user_viewed(self, timestamp):
        user = self.request.user
        if not user.is_authenticated:
            return
        if UserProductTimestamp.objects.filter(user=user).count() == 12:
            UserProductTimestamp.objects.filter(user=user).order_by("timestamp").first().delete()
        upt, _ = UserProductTimestamp.objects.get_or_create(user=user, product=self.get_object())
        upt.timestamp = timestamp
        upt.save()
        return upt.timestamp


class ProductSearchView(ListView):
    template_name = "Products/Product_list.html"
    context_object_name = "products"
    extra_context = {"banner_title": "Search Results"}
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        get_copy = self.request.GET.copy()
        parameters = get_copy.pop("page", True) and get_copy.urlencode()
        context["parameters"] = parameters
        return context

    def get_queryset(self):
        if self.request.GET.get("q"):
            query = self.request.GET.get("q")
            return Product.products.filter(Q(title__icontains=query))


class ProductCategoryView(ListView):
    template_name = "Products/Product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.products.filter(category__slug=self.kwargs["category"])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["banner_title"] = Category.objects.get(slug=self.kwargs["category"]).title
        return context


class ProductOnSaleView(ListView):
    template_name = "Products/Product_list.html"
    context_object_name = "products"
    extra_context = {"banner_title": "On Sale Products"}
    
    def get_queryset(self):
        return Product.products.filter(discount__isnull=False)


class ProductTopSellersView(ListView):
    template_name = "Products/Product_list.html"
    context_object_name = "products"
    extra_context = {"banner_title": "Top Sellers"}
    paginate_by = 12
    
    def get_queryset(self):
        return Product.products.filter(sold__gt=0).order_by("-sold")

    
class ProductRecentlyViewdView(LoginRequiredMixin, ListView):
    template_name = "Products/Product_list.html"
    context_object_name = "products"
    extra_context = {"banner_title": "Recently Viewed Products"}
    paginate_by = 12
    
    def get_queryset(self):
        return Product.products.filter(timestamps__user=self.request.user).order_by("-timestamps__timestamp")


class ProductBrandView(ListView):
    template_name = "Products/Product_list.html"
    context_object_name = "products"
    paginate_by = 12
    
    def get_queryset(self):
        return Product.products.filter(brand__slug=self.kwargs["brand"])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["banner_title"] = Brand.objects.get(slug=self.kwargs["brand"]).title
        return context