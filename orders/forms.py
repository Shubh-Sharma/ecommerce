from django import forms
from django.contrib.auth import get_user_model

from .models import UserAddress

User = get_user_model()


class GuestCheckoutForm(forms.Form):
	email = forms.EmailField()
	email2 = forms.EmailField(label="Confirm Email")

	def clean_email2(self):
		email = self.cleaned_data.get("email")
		email2 = self.cleaned_data.get("email2")
		if email == email2:
			user_exists = User.objects.filter(email=email).count()
			if user_exists != 0:
				raise forms.ValidationError("User already exists. Please Login instead.")
			return email2
		else:
			raise forms.ValidationError("Confirmation Email doesn't match")



class AddressForm(forms.Form):
	billing_address = forms.ModelChoiceField(queryset=UserAddress.objects.filter(type="billing"), empty_label=None, widget=forms.RadioSelect)
	shipping_address = forms.ModelChoiceField(queryset=UserAddress.objects.filter(type="shipping"), empty_label=None, widget=forms.RadioSelect)
	# billing_address = forms.CharField(max_length=220)
	# shipping_address = forms.CharField(max_length=220)


class UserAddressForm(forms.ModelForm):
	class Meta:
		model = UserAddress
		fields = [
			'street',
			'city',
			'state',
			'pincode',
			'type',
		]