import qrcode
import datetime
from django.db import models
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw


class Category(models.Model):
    """Store the category of the product"""
    title = models.CharField(max_length=200)

    def __str__(self):
        """Return string representation of the category"""
        return self.title


class Product(models.Model):
    """Store the product information"""
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    p_image = models.ImageField(upload_to='products')
    price = models.PositiveIntegerField()
    code = models.CharField(max_length=200)
    in_stock = models.PositiveIntegerField()

    def __str__(self):
        """Return string representation of the product"""
        return self.title


class Cart(models.Model):
    """store cart information"""
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string representation of the cart"""
        return 'Cart' + str(self.id)


class CartProduct(models.Model):
    """Store the cart product"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        """Return string representation of the cart product"""
        return 'Cart: ' + str(self.cart.id) + 'Cart product: ' + str(self.id)


class Order(models.Model):
    """Store order information"""
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    phone = models.CharField(max_length=200)
    subtotal = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    qr_image = models.ImageField(upload_to='qr_image', blank=True, null=True)

    def __str__(self):
        """Return string representation of the order"""
        return 'Order: ' + str(self.id)

    def save(self, *args, **kwargs):
        """overriding the save method for QR code"""

        now = datetime.datetime.now()
        qr_image = qrcode.make(f'Date:{now}\nName:{self.customer_name}\nEmail:{self.email}\nPhone:{self.phone}')
        canvas = Image.new('RGB', (500, 500), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qr_image)
        fname = f'qr_image-{self.phone}' + '.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_image.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)
