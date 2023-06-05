from django.db import models
from django.utils.safestring import mark_safe


class ProductCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Color(models.Model):
    color = models.CharField(max_length=50)
    normal_repr = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.normal_repr} {self.color}"

    class Meta:
        verbose_name = "Цвета"
        verbose_name_plural = "Цвета"


class Size(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Размеры"
        verbose_name_plural = "Размеры"


class Product(models.Model):
    SEX = [
        (1, "Мужской"),
        (2, "Женский"),
        (3, "Унисекс")
    ]

    image = models.ImageField(upload_to="products_title_img", verbose_name="Заголовочное фото")
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    color = models.ForeignKey(to=Color, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=9, decimal_places=3, default=0)
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)
    sex = models.PositiveSmallIntegerField("Пол", choices=SEX)
    size = models.ForeignKey(to=Size, default=1, on_delete=models.CASCADE)
    quantity_in_stock = models.IntegerField(default=0, verbose_name="Количество на складе")

    @property
    def html_colors_represent(self):
        products = Product.objects.filter(title=self.title)
        result = []
        for product in products:
            result.append((mark_safe(f"<div style='display: inline-block;"
                                    f"margin-right: 0.2vw;"
                                    f"width: 1vw;height: 1vw;"
                                    f"-webkit-border-radius: 25px;"
                                    f"-moz-border-radius: 25px;"
                                    f"border-radius: 25px;"
                                    f"background: {product.color.color};border:"
                                    f" 2px solid gray;'></div>"), product.color.color))
        return result

    @property
    def similar(self):
        result = Product.objects.filter(color=self.color, category=self.category).exclude(pk=self.pk)
        if len(result) < 4:
            result = Product.objects.filter(category=self.category).exclude(pk=self.pk)
        return result
        # TODO: in future more logical

    @property
    def sizes(self):
        result_lst = []
        for product in Product.objects.filter(title=self.title):
            result_lst.append((product.size, product.size.pk))

        return result_lst

    @property
    def product_images(self):
        return ProductImages.objects.filter(product=self)

    def __str__(self):
        return f"Название: {self.title}, размер: {self.size}, цвет: {self.color}"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ProductImages(models.Model):
    image = models.ImageField(upload_to='product_images/%Y/%m/%d')
    product = models.ManyToManyField(to=Product)

    def __str__(self):
        return f"Фото: {self.image}"

    class Meta:
        verbose_name = "Фото товара"
        verbose_name_plural = "Фотографии товара"
