from django.db import models

class Branch(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)

class Staff(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=50, default='Master') # 'Admin Master' or 'Master'

class Student(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    beltRank = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)

class Lead(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    program = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='New')

class Invoice(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.IntegerField()
    status = models.CharField(max_length=50, default='Pending') # 'Paid' or 'Pending'
    description = models.CharField(max_length=200, default='Monthly Tuition')
    date_issued = models.DateField(auto_now_add=True)
