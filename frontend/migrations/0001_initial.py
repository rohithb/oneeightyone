# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('customernumber', models.IntegerField(serialize=False, db_column='customerNumber', primary_key=True)),
                ('customername', models.CharField(db_column='customerName', max_length=50)),
                ('contactlastname', models.CharField(db_column='contactLastName', max_length=50)),
                ('contactfirstname', models.CharField(db_column='contactFirstName', max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('addressline1', models.CharField(db_column='addressLine1', max_length=50)),
                ('addressline2', models.CharField(null=True, blank=True, db_column='addressLine2', max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(null=True, blank=True, max_length=50)),
                ('postalcode', models.CharField(null=True, blank=True, db_column='postalCode', max_length=15)),
                ('country', models.CharField(max_length=50)),
                ('creditlimit', models.FloatField(null=True, blank=True, db_column='creditLimit')),
            ],
            options={
                'db_table': 'customers',
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
            },
        ),
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('employeenumber', models.IntegerField(serialize=False, db_column='employeeNumber', primary_key=True)),
                ('lastname', models.CharField(db_column='lastName', max_length=50)),
                ('firstname', models.CharField(db_column='firstName', max_length=50)),
                ('extension', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=100)),
                ('jobtitle', models.CharField(db_column='jobTitle', max_length=50)),
            ],
            options={
                'db_table': 'employees',
            },
        ),
        migrations.CreateModel(
            name='Offices',
            fields=[
                ('officecode', models.CharField(serialize=False, db_column='officeCode', primary_key=True, max_length=10)),
                ('city', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('addressline1', models.CharField(db_column='addressLine1', max_length=50)),
                ('addressline2', models.CharField(null=True, blank=True, db_column='addressLine2', max_length=50)),
                ('state', models.CharField(null=True, blank=True, max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('postalcode', models.CharField(db_column='postalCode', max_length=15)),
                ('territory', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'offices',
            },
        ),
        migrations.CreateModel(
            name='Orderdetails',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('quantityordered', models.IntegerField(db_column='quantityOrdered')),
                ('priceeach', models.FloatField(db_column='priceEach')),
                ('orderlinenumber', models.SmallIntegerField(db_column='orderLineNumber')),
            ],
            options={
                'db_table': 'orderdetails',
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('ordernumber', models.IntegerField(serialize=False, db_column='orderNumber', primary_key=True)),
                ('orderdate', models.DateField(db_column='orderDate')),
                ('requireddate', models.DateField(db_column='requiredDate')),
                ('shippeddate', models.DateField(null=True, blank=True, db_column='shippedDate')),
                ('status', models.CharField(max_length=15)),
                ('comments', models.TextField(null=True, blank=True)),
                ('customernumber', models.ForeignKey(to='frontend.Customers', db_column='customerNumber')),
            ],
            options={
                'db_table': 'orders',
            },
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('checknumber', models.CharField(db_column='checkNumber', max_length=50)),
                ('paymentdate', models.DateField(db_column='paymentDate')),
                ('amount', models.FloatField()),
                ('customernumber', models.ForeignKey(to='frontend.Customers', db_column='customerNumber')),
            ],
            options={
                'db_table': 'payments',
            },
        ),
        migrations.CreateModel(
            name='Productlines',
            fields=[
                ('productline', models.CharField(serialize=False, db_column='productLine', primary_key=True, max_length=50)),
                ('textdescription', models.CharField(null=True, blank=True, db_column='textDescription', max_length=4000)),
                ('htmldescription', models.TextField(null=True, blank=True, db_column='htmlDescription')),
                ('image', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'productlines',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('productcode', models.CharField(serialize=False, db_column='productCode', primary_key=True, max_length=15)),
                ('productname', models.CharField(db_column='productName', max_length=70)),
                ('productscale', models.CharField(db_column='productScale', max_length=10)),
                ('productvendor', models.CharField(db_column='productVendor', max_length=50)),
                ('productdescription', models.TextField(db_column='productDescription')),
                ('quantityinstock', models.SmallIntegerField(db_column='quantityInStock')),
                ('buyprice', models.FloatField(db_column='buyPrice')),
                ('msrp', models.FloatField(db_column='MSRP')),
                ('productline', models.ForeignKey(to='frontend.Productlines', db_column='productLine')),
            ],
            options={
                'db_table': 'products',
            },
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='ordernumber',
            field=models.ForeignKey(to='frontend.Orders', db_column='orderNumber'),
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='productcode',
            field=models.ForeignKey(to='frontend.Products', db_column='productCode'),
        ),
        migrations.AddField(
            model_name='employees',
            name='officecode',
            field=models.ForeignKey(to='frontend.Offices', db_column='officeCode'),
        ),
        migrations.AddField(
            model_name='employees',
            name='reportsto',
            field=models.ForeignKey(null=True, to='frontend.Employees', db_column='reportsTo', blank=True),
        ),
        migrations.AddField(
            model_name='customers',
            name='salesrepemployeenumber',
            field=models.ForeignKey(null=True, to='frontend.Employees', db_column='salesRepEmployeeNumber', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='payments',
            unique_together=set([('customernumber', 'checknumber')]),
        ),
        migrations.AlterUniqueTogether(
            name='orderdetails',
            unique_together=set([('ordernumber', 'productcode')]),
        ),
    ]
