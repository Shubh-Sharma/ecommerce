from decimal import Decimal
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from products.models import Variation
# Create your models here.


class CartItem(models.Model):
	cart = models.ForeignKey("Cart")
	item = models.ForeignKey(Variation)
	quantity = models.PositiveIntegerField(default=1)
	line_item_total = models.DecimalField(max_digits=10, decimal_places=2)


	def __unicode__(self):
		return self.item.title

	def remove(self):
		return self.item.remove_from_cart()

	def get_title(self):
		product_name = self.item.product.title
		variation_name = self.item.title
		if variation_name == "Default":
			return "%s" %(product_name)
		else:
			return "%s %s" %(product_name, variation_name)


def cart_item_pre_save_reciever(sender, instance, *args, **kwargs):
	qty = instance.quantity
	if qty >= 1:
		price = instance.item.get_price()
		line_item_total = Decimal(qty) * Decimal(price)
		instance.line_item_total = line_item_total


pre_save.connect(cart_item_pre_save_reciever, sender=CartItem)


def cart_item_post_save_reciever(sender, instance, *args, **kwargs):
	instance.cart.update_subtotal()


post_save.connect(cart_item_post_save_reciever, sender=CartItem)

post_delete.connect(cart_item_post_save_reciever, sender=CartItem)




class Cart(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
	items = models.ManyToManyField(Variation, through=CartItem)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	subtotal = models.DecimalField(max_digits=50, decimal_places=2, default=25.00) # remove null=True later
	tax_percentage = models.DecimalField(max_digits=10, decimal_places=5, default=0.085)
	tax_total = models.DecimalField(max_digits=50, decimal_places=2, default=25.00)
	total = models.DecimalField(max_digits=50, decimal_places=2, default=25.00)
	# discounts
	# shipping

	def __unicode__(self):
		return str(self.id)

	def update_subtotal(self):
		subtotal = 0
		items = self.cartitem_set.all()
		for item in items:
			subtotal += item.line_item_total
		self.subtotal = subtotal
		self.save()




def do_tax_and_total_reciever(sender, instance, *args, **kwargs):
	subtotal = Decimal(instance.subtotal)
	tax_total = round(subtotal * Decimal(instance.tax_percentage), 2)
	total = round(subtotal + Decimal(tax_total), 2)
	instance.tax_total = "%.2f"% (tax_total)
	instance.total = "%.2f"% (total)


pre_save.connect(do_tax_and_total_reciever, sender=Cart)














