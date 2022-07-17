from django import forms
from django.contrib import admin, messages
from django.contrib.admin.helpers import ActionForm
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

from .models import Category, Product, ProductImage, Brand, Slider

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Slider)

class ProductImageInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        data = self.cleaned_data
        count = 0
        empty = 0
        for image in data:
            if not bool(image):
                empty += 1
                continue
            if image.get("is_feature", None):
                count += 1
        if empty == len(data):
            raise forms.ValidationError("At least one image is required for product.")
        if count > 1:
            raise forms.ValidationError("Only one image can have is_feature set.")
        if count == 0:
            raise forms.ValidationError("One image required to be set as is_feature.")


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    max_num = 4
    formset = ProductImageInlineFormset


class DiscountFilter(admin.SimpleListFilter):
    title = _("Discount")
    parameter_name = "discount"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ("true", "With discount"),
            ("false", "Without discount"),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == "true":
            return queryset.filter(discount__isnull=False)
        if self.value() == "false":
            return queryset.filter(discount__isnull=True)


class DiscountActionForm(ActionForm):
    discount = forms.IntegerField(
        label=_("Discount:"),
        max_value=99,
        min_value=1,
        help_text=_("Discount in percent from 1 to 99"),
        validators=[MaxValueValidator(99), MinValueValidator(1)],
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    exclude = ("final_price",)
    list_display = (
        "title",
        "created_at",
        "category",
        "brand",
        "sold",
        "quantity",
        "regular_price",
        "discount",
        "final_price",
        "is_active",
    )
    list_editable = ("regular_price", "is_active")
    list_filter = ("category", "is_active", "in_stock", DiscountFilter)
    search_fields = [
        "title",
    ]
    inlines = [ProductImageInline]
    action_form = DiscountActionForm
    actions = ["set_discount_on_products", "delete_selected"]

    @admin.action(description=_("Set discount on selected products"))
    def set_discount_on_products(self, request, queryset):
        discount = int(request.POST.get("discount"))
        queryset.update(discount=discount)
        count = queryset.count()
        for product in queryset:
            product.save()
        if count == 1:
            messages.success(request, "Discount applied to 1 product.")
        elif count > 1:
            messages.success(request, f"Discount applied to {count} products.")
