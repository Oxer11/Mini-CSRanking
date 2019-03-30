from django.db import models

# Create your models here.

class School(models.Model):
    name = models.CharField(primary_key=True, max_length=30)

    class Meta:
        db_table = 'school'
        verbose_name = '学校信息'
        verbose_name_plural = '学校信息'
        ordering = ['name']

class Author(models.Model):
    name = models.CharField(primary_key=True, max_length=30)
    title = models.CharField(max_length=20)
    email = models.EmailField()
    homepage = models.URLField()
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    class Meta:
        db_table = 'author'
        verbose_name = '作者信息'
        verbose_name_plural = '作者信息'
        ordering = ['name']

class Conference(models.Model):
    cid = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50)
    abbr = models.CharField(max_length=10)
    year = models.PositiveIntegerField(null=False)
    domain = models.CharField(max_length=40)
    page = models.URLField()

    class Meta:
        db_table = 'conference'
        verbose_name = ' 会议信息'
        verbose_name_plural = '会议信息'
        ordering = ['name']

class Journal(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    abbr = models.CharField(max_length=10)
    year = models.PositiveIntegerField()
    domain = models.CharField(max_length=40)
    publisher = models.CharField(max_length=20)

    class Meta:
        db_table = 'journal'
        verbose_name = ' 期刊信息'
        verbose_name_plural = '期刊信息'
        ordering = ['name']

class Paper(models.Model):
    pid = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50)
    keywords = models.CharField(max_length=50)

class Authorship(models.Model):
    pid = models.ForeignKey(Paper, on_delete=models.CASCADE)
    aid = models.ForeignKey(Author, on_delete=models.CASCADE)