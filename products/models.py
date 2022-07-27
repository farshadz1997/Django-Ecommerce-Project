from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Prefetch
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from PIL import Image


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().prefetch_related(Prefetch(
            "images", 
            ProductImage.objects.filter(is_feature=True), 
            "main_image")).filter(is_active=True)


class Product(models.Model):
    title = models.CharField(_("Title"), max_length=255)
    quantity = models.PositiveIntegerField(_("Quantity"), default=1)
    sold = models.PositiveIntegerField(_("Sold"), default=0)
    category = models.ForeignKey("Category", related_name="products", verbose_name=_("Category"), on_delete=models.CASCADE)
    brand = models.ForeignKey("Brand", related_name="products", verbose_name=_("Brand"), on_delete=models.CASCADE, null=True)
    regular_price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    discount = models.PositiveIntegerField(
        _("Discount"), blank=True, null=True, validators=[MaxValueValidator(99), MinValueValidator(1)]
    )
    final_price = models.DecimalField(_("Final price"), max_digits=10, decimal_places=2, blank=True, null=True)
    description = RichTextField()
    slug = AutoSlugField(populate_from="title", unique=True)
    in_stock = models.BooleanField(default=True, verbose_name="Availability in stock")
    is_active = models.BooleanField(_("Product visibility"), default=True)
    objects = models.Manager()
    products = ProductManager()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    user_wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_wishlist", verbose_name="User wishlist", blank=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ["-created_at"]
        default_manager_name = "products"
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("products:product_detail", kwargs={"pk": self.pk, "slug": self.slug})

    def get_featured_image(self):
        obj = self.images.filter(is_feature=True).first()
        image = obj.image
        alt = obj.alt_text
        return {"image": image, "alt_text": alt}

    def save(self, *args, **kwargs):
        self.final_price = self.regular_price
        if self.discount != None:
            self.final_price = self.regular_price - (self.regular_price * self.discount / 100)
        super(Product, self).save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", verbose_name=_("Product"), on_delete=models.CASCADE)
    image = models.ImageField(verbose_name=_("Image"), help_text=_("Upload a product image"), upload_to="products/")
    alt_text = models.CharField(
        verbose_name=_("Alternative text"),
        help_text=_("Please add alternative text"),
        max_length=255,
        null=True,
        blank=True,
    )
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if self.alt_text is None:
            self.alt_text = self.product.title
        super(ProductImage, self).save(*args, **kwargs)
        img = Image.open(self.image)
        if img.width > 400 or img.height > 500:
            output_size = (400, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = AutoSlugField(populate_from="title")
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("products:product_category", kwargs={"category": self.slug})


class Brand(models.Model):
    title = models.CharField(_("Ttile"), max_length=255, unique=True)
    image = models.ImageField(verbose_name=_("Image"), help_text=_("Upload brand image or logo"), upload_to="brands/")
    slug = AutoSlugField(populate_from="title")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    
    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("products:product_brand", kwargs={"brand":self.slug})
    
    def save(self, *args, **kwargs):
        super(Brand, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.width > 270 or img.height > 120:
            output_size = (270, 120)
            final_image = img.resize(output_size)
            final_image.save(self.image.path)
    
    
class UserProductTimestamp(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="timestamps")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="timestamps")
    timestamp = models.DateTimeField(_("Time Stamp"), blank=True, null=True)
    

class Slider(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="slider", verbose_name=_("Product"))
    feature = models.CharField(_("Feature"), max_length=50, help_text=_("Any special feature"), blank=True, null=True)
    subtitle = models.CharField(_("Subtitle"), max_length=50, help_text=_("few detail"), blank=True, null=True)
    image = models.ImageField(_("Slider image"), help_text=_("Upload a product image"), upload_to="slider/")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    
    class Meta:
        verbose_name = _("Slider")
        verbose_name_plural = _("Sliders")
        
    def __str__(self):
        return self.product.title
    
    def save(self, *args, **kwargs):
        super(Slider, self).save(*args, **kwargs)
        img = Image.open(self.image)
        if img.width > 1200 or img.height > 600:
            output_size = (1200, 600)
            img.thumbnail(output_size)
            img.save(self.image.path)