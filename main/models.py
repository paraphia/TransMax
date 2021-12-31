from django.db import models

class Product(models.Model):
	name    = models.TextField('Название продукта')
	link    = models.TextField('Ссылка')
	count   = models.IntegerField('Проданное количество')
	price   = models.IntegerField('Цена')
	income  = models.BigIntegerField('Прибыль')
	created_at  = models.DateTimeField(auto_now_add=True)
	updated_at  = models.DateTimeField(auto_now = True)

	def __str__(self):
		return self.name
class ArchiveIncome(models.Model):
	archive_parent   = models.ForeignKey(Product, on_delete=models.CASCADE) 
	archive_count    = models.IntegerField()
	archive_bill     = models.BigIntegerField()
	archive_income   = models.BigIntegerField('Прибыль')
	archive_increase = models.IntegerField()	
	archive_income_increase = models.IntegerField()	
	archive_created_at  = models.DateTimeField(auto_now_add = True)
	
	def __str__(self):
		return self.archive_bill
		
class TotalIncome(models.Model):
	date  = models.DateTimeField(auto_now_add = True)
	sales = models.IntegerField()
	bill  = models.BigIntegerField()