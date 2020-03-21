from django.db import models

class Industry(models.Model):
    industry_field = models.CharField(max_length=64)

class Company(models.Model):
    company_name = models.CharField(max_length=64)
    industry_from = models.ForeignKey(
        Industry,
        on_delete=models.CASCADE
    )

class User(models.Model):
    username = models.CharField(max_length=64)
    password_hash = models.CharField(max_length=64)
    email = models.CharField(max_length=64)

class Post(models.Model):
    body = models.TextField()
    timestamp = models.DateTimeField()
    company_about = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        null=True
    )
    posted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

class Comment(models.Model):
    body = models.TextField()
    timestamp = models.DateTimeField()
    is_positive = models.BooleanField()
    commented_on = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    commented_by = models.ForeignKey(
        User,
        on_delete = models.CASCADE
    )

