from django.db.models import Q
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

# Create your views here.


from .models import Product, Variation



class VariationListView(ListView):
	model = Variation
	queryset = Variation.objects.all()

	# def get_context_data(self, *args, **kwargs):
	# 	context = super(VariationListView, self).get_context_data(*args, **kwargs)
	# 	context["now"] = timezone.now()
	# 	context["query"] = self.request.GET.get("q")
	# 	return context

	def get_queryset(self, *args, **kwargs):
		qs = super(VariationListView, self).get_queryset(*args, **kwargs)
		query = self.request.GET.get("q")
		return qs




class ProductListView(ListView):
	model = Product

	def get_context_data(self, *args, **kwargs):
		context = super(ProductListView, self).get_context_data(*args, **kwargs)
		context["now"] = timezone.now()
		context["query"] = self.request.GET.get("q")
		return context


	def get_queryset(self, *args, **kwargs):
		# used super call to get default queryset
		qs = super(ProductListView, self).get_queryset(*args, **kwargs)
		# check if user searched for a query and get it 
		query = self.request.GET.get("q")
		if query:
			qs = self.model.objects.filter(
					Q(title__icontains=query)|
					Q(description__icontains=query)
				)
			try:
				qs2 = self.model.objects.filter(
					Q(price=query)
				)
				qs = (qs | qs2).distinct()
			except:
				pass
		return qs


class ProductDetailView(DetailView):
	model = Product
	# template_name = "<appname>/<modulename>_detail.html"


def product_detail_view(request, id):
	# product_instance = get_object_or_404(Product, id=id)
	try:
		product_instance = Product.objects.get(id=id)
	except Product.DoesNotExist:
		raise Http404
	except:
		raise Http404
	template = "products/product_detail.html"
	context = {
		"object": product_instance
	}
	return render(request, template, context)