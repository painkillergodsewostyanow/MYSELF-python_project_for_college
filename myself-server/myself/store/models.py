from django.db import models
from django.utils.safestring import mark_safe


class ProductCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


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

    image = models.ImageField(upload_to="products_title_img")
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField()
    cost = models.DecimalField(max_digits=9, decimal_places=3, default=0)
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)
    sex = models.PositiveSmallIntegerField("Пол", choices=SEX)
    size = models.ForeignKey(to=Size, default=1, on_delete=models.CASCADE)
    quantity_in_stock = models.IntegerField(default=0, verbose_name="Количество на складе")

    @property
    def html_colors_represent(self):

        colors = Color.objects.filter(pk=self.pk)
        result = ""
        for color in colors:
            result += f"<div style='display: inline-block;" \
                      f"margin-right: 0.2vw;" \
                      f"width: 1vw;height: 1vw;" \
                      f"-webkit-border-radius: 25px;" \
                      f" -moz-border-radius: 25px;" \
                      f"border-radius: 25px;" \
                      f"background: {color.hex};border:" \
                      f" 2px solid gray;'></div>"
        return mark_safe(result)

    def __str__(self):
        return f"Название: {self.title}, размер: {self.size}"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Color(models.Model):
    hex = models.CharField(max_length=50)
    normal_repr = models.CharField(max_length=50)
    product = models.ManyToManyField(to=Product)

    def __str__(self):
        return f"{self.normal_repr} {self.hex}"

    class Meta:
        verbose_name = "Цвета"
        verbose_name_plural = "Цвета"


class ProductImages(models.Model):
    image = models.ImageField(upload_to='product_images/%Y/%m/%d')
    product = models.ManyToManyField(to=Product)

    def __str__(self):
        return f"Фото: {self.image}"

    class Meta:
        verbose_name = "Фото товара"
        verbose_name_plural = "Фотографии товара"
