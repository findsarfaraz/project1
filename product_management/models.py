from __future__ import unicode_literals

from django.db import models
from user_management.models import CustomUser


# Create your models here.
class product_master(models.Model):
	product_id = models.AutoField(primary_key=True)
	product_name=models.CharField(max_length=512,null =False,blank=False)
	product_description=models.CharField(max_length=4000)
	product_type =models.CharField(max_length=200)
	product_color =models.CharField(max_length=200)
	product_patern =models.CharField(max_length=200)
	category_id	=models.IntegerField()
	subcateogry_category_id	=models.IntegerField()
	sale_flag =models.BooleanField(default=False)
	creation_date= models.DateTimeField(auto_now=True,editable=False,blank=False,null=False)
	updation_date= models.DateTimeField(auto_now=True,editable=False,blank=False,null=False)
	created_by = models.ForeignKey(CustomUser)

class product_image_master(models.Model):
	product_image_id =models.AutoField(primary_key=True)
	product_id =models.ForeignKey(CustomUser)
	product_image_path=models.FileField()
	product_id = models.ForeignKey(product_master)

class product_price_history(models.Model):
	product_price_id =models.AutoField(primary_key=True)
	product_id =models.ForeignKey(product_master)
	product_price=models.FloatField()
	effective_date=models.DateTimeField(blank=False,null=False)
	creation_date= models.DateTimeField(auto_now=True,editable=False,blank=False,null=False)
	updation_date= models.DateTimeField(auto_now=True,editable=False,blank=False,null=False)
	created_by = models.ForeignKey(CustomUser)


class category(models.Model):
	category_id= models.AutoField(primary_key=True)
	category_name =models.CharField(max_length=512,null=False)

class subcategory(models.Model):
	subcategory_id= models.AutoField(primary_key=True)
	subcategory_name =models.CharField(max_length=512,null=False)
	category_id =models.ForeignKey(category)
	






