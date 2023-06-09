from django.db import models


class ProductImages(models.Model):
    image = models.ImageField(upload_to='product_images/%Y/%m/%d')

    def __str__(self):
        return f"Фото: {self.image}"

    class Meta:
        verbose_name = "Фото товара"
        verbose_name_plural = "Фотографии товара"


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
    color = models.ForeignKey(to=Color, on_delete=models.CASCADE, verbose_name="Цвет")
    cost = models.DecimalField(max_digits=9, decimal_places=3, default=0, verbose_name="Цена")
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE, verbose_name="Категория")
    sex = models.PositiveSmallIntegerField(choices=SEX, verbose_name="Пол")
    sizes = models.ManyToManyField(to=Size, verbose_name="Доступные размеры")
    detail_images = models.ManyToManyField(to=ProductImages)

    @property
    def get_sizes(self):
        return self.sizes.all()

    @property
    def get_colors(self):
        products = Product.objects.filter(title=self.title)

        result = []
        for product in products:
            result.append(product.color)

        return result

    @property
    def similar(self):
        result = Product.objects.filter(color=self.color, category=self.category).exclude(pk=self.pk)
        if len(result) < 4:
            result = Product.objects.filter(category=self.category).exclude(pk=self.pk)

        return self.del_duplicate_by_title(result)
        # TODO: in future more logical

    @staticmethod
    def del_duplicate_by_title(queryset):
        product_lst = []
        product_titles_lst = []

        for product in queryset:
            if product.title in product_titles_lst:
                continue

            product_titles_lst.append(product.title)
            product_lst.append(product)

        return product_lst

    @property
    def product_images(self):
        return self.detail_images.all()

    def __str__(self):
        return f"Название: {self.title} цвет: {self.color}"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
