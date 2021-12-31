import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook
import os
import django
from multiprocessing.dummy import Pool as ThreadPool 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "transmax.settings")
django.setup()
from main.models import Product, TotalIncome, ArchiveIncome
from django.db.models import Avg, Count, Min, Sum
page_url = 'https://videohive.net/user/transmaxx/portfolio?direction=desc&order_by=sortable_at&page=1&view=grid'
def get_page(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.content,'html.parser')
	uls = soup.find('ul',{'class':'product-grid'})
	uls_soup = BeautifulSoup(str(uls),'html.parser')
	divs = uls_soup.findAll('div',{'class':'product-grid__inside'})
	# print(uls_soup)
	for div in divs:
		div_soup = BeautifulSoup(str(div),'html.parser')
		product_heading = div_soup.find('h3',{'class':'product-grid__heading'})
		product_heading_soup = BeautifulSoup(str(product_heading),'html.parser')
		link = product_heading_soup.find('a')['href']
		link = "https://videohive.net"+str(link)
		product_sales   = div_soup.find('footer',{'class':'product-grid__footer'})
		product_price   = div_soup.find('span',{'class':'product-grid__price'})
		#Фильтрация данных	
		product_sales = str(product_sales.text).replace('\n','')
		product_heading = product_heading.text.rstrip(' \n').lstrip(' \n')
		try:
			sales = int((str(product_sales).split('Sales')[0]))
		except:
			sales = int((str(product_sales).split('Sale')[0]))
		product_price = int(str(product_price.text).replace('$',''))
		try:
			product = Product.objects.get(link = link)
		except:
			product = None
		if product == None:
			product = Product.objects.create(name =product_heading,link=link,count =sales,price = product_price,income = product_price*sales)
			# Income.objects.create(product=product,count = count = int(sales),bill = int(product_price),income = product_price*sales)
			print("Insert: "+str(product_heading)+' | '+str(product.count)+' | '+str(product.price))
		else:
			if product.count == sales:
				print('Нету изменений....')
			else:
				print('|- Есть именения в продаже....'+str(sales)+" к "+str(product.count))
				difference = sales - product.count
				income_differece = product_price*sales - product.income
				ArchiveIncome.objects.create(archive_parent = product,archive_count = sales,archive_bill= product_price,archive_income =product_price*sales ,archive_increase = difference,archive_income_increase = income_differece)
			product.name = product_heading
			product.count = sales
			product.link = link
			product.price = product_price
			product.income = product_price*sales
			product.save()

			print("Update: "+str(product_heading)+' | '+str(product.count)+' | '+str(product.price))
page = requests.get(page_url)
soup = BeautifulSoup(page.content,'html.parser')
uls = soup.find('ul',{'class':'pagination__list'})
uls_soup = BeautifulSoup(str(uls),'html.parser')
lis = uls_soup.findAll('a',{'class','pagination__page'})
last_one = lis[len(lis)-1]
page_count = int(last_one.text)
print(page_count)
page_urls = []
for page in range(1,page_count+1):
	page_url = 'https://videohive.net/user/transmaxx/portfolio?direction=desc&order_by=sortable_at&page='+str(page)+'&view=grid'
	get_page(page_url)
print('Суммирование общего заработка...')
total_income = Product.objects.all().aggregate(Sum('income'))
total_sales = Product.objects.all().aggregate(Sum('count'))
TotalIncome.objects.create(bill = total_income['income__sum'],sales = total_sales['count__sum'])
print('.....ГОТОВО.....')