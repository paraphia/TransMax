from django.shortcuts import render, get_object_or_404
import datetime
from .models import Product, TotalIncome,ArchiveIncome
def index(request):
	week_day = datetime.datetime.now().isocalendar()[2]
	start_date = datetime.datetime.now() - datetime.timedelta(days = week_day)
	dates = [str((start_date+datetime.timedelta(days=i)).date()) for i in range(8)]
	dates = dates[1:]
	totals = TotalIncome.objects.all().order_by('-id')
	difference = totals[0].bill - totals[len(totals)-1].bill
	changes = ArchiveIncome.objects.all().order_by('-id')
	return render(request,'main/index.html',{'days':dates,'totals':totals,'changes':changes,'difference':difference})
def list(request):
	products_list = Product.objects.all().order_by('-count')
	return render(request,'main/list.html',{'products_list':products_list})
def product(request,pid):
	week_day = datetime.datetime.now().isocalendar()[2]
	start_date = datetime.datetime.now() - datetime.timedelta(days = week_day)
	dates = [str((start_date+datetime.timedelta(days=i)).date()) for i in range(8)]
	dates = dates[1:]
	products = get_object_or_404(Product, pk=pid)
	product_changes = products.archiveincome_set.all()
	return render(request,'main/product.html',{'product':products,'product_changes':product_changes,'days':dates})