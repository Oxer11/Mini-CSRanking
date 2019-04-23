from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Institution(models.Model):
    name = models.CharField(primary_key=True, max_length=30)
    homepage = models.URLField(blank=True, null=True)
    pub_cnt = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'institution'
        verbose_name = '机构信息'
        verbose_name_plural = '机构信息'
        ordering = ["-pub_cnt", 'name']

class Scholar(models.Model):
    name = models.CharField(primary_key=True, max_length=30)
    homepage = models.URLField(blank=True, null=True)
    DBLP = models.URLField(blank=True, null=True)
    GoogleScholar = models.URLField(blank=True, null=True)
    affiliation = models.ForeignKey(Institution, on_delete=models.CASCADE)
    pub_cnt = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'scholar'
        verbose_name = '学者信息'
        verbose_name_plural = '学者信息'
        ordering = ['-pub_cnt', "name"]
		
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	scholar = models.OneToOneField(Scholar, on_delete=models.CASCADE, null=True, blank=True)
	gender = models.CharField(max_length=10, choices=(("M", 'Male'), ("F", 'Female')), default='M')
	identity = models.CharField(max_length=10, choices=(("P", 'Professor'), ("S", u'Student')), default='S')
	institution = models.CharField(max_length=100, blank=True, null=True)
	
	def __str__(self):
		return self.user.username

	class Meta:
		db_table = 'profile'
		verbose_name = '用户信息'
		verbose_name_plural = '用户信息'
		ordering = ['user']

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user = instance)
		
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

class Conference(models.Model):
    name = models.CharField(max_length=50)
    abbr = models.CharField(max_length=10)
    year = models.PositiveIntegerField(null=False)
    DBLP = models.URLField(blank=True, null=True)
    Href = models.URLField(blank=True, null=True)

    def __str__(self):
        return u"%s%d"%(self.abbr, self.year)

    class Meta:
        db_table = 'conference'
        verbose_name = '会议信息'
        verbose_name_plural = '会议信息'
        ordering = ['name', '-year']

class Paper(models.Model):
    title = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    href = models.URLField(max_length=500)
    conf_id = models.ForeignKey(Conference, on_delete=models.CASCADE)

    def __str__(self):
        return u"%s %s%d"%(self.title, self.conf_id.abbr, self.year)

    class Meta:
        db_table = 'paper'
        verbose_name = '论文信息'
        verbose_name_plural = '论文信息'
        ordering = ['-year']

class Area(models.Model):
    name = models.CharField(max_length=50)
    direction = models.CharField(max_length=50)

    def __str__(self):
        return u"%s %s"%(self.name, self.direction)

    class Meta:
        db_table = 'area'
        verbose_name = '领域信息'
        verbose_name_plural = '领域信息'
        ordering = ['name']

class Scholar_Paper(models.Model):
    scholar_name = models.ForeignKey(Scholar, on_delete=models.CASCADE)
    paper_title = models.ForeignKey(Paper, on_delete=models.CASCADE)

    def __str__(self):
        return u"%s %s"%(self.scholar_name, self.paper_title)

    class Meta:
        db_table = 'scholar_paper'
        verbose_name = '作者-论文信息'
        verbose_name_plural = '作者-论文信息'
        ordering = ['paper_title', 'scholar_name']

class Scholar_Area(models.Model):
    scholar_name = models.ForeignKey(Scholar, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)

    def __str__(self):
        return u"%s %s"%(self.scholar_name.name, self.area.name)

    class Meta:
        db_table = 'scholar_area'
        verbose_name = '作者-领域信息'
        verbose_name_plural = '作者-领域信息'
        ordering = ['area', 'scholar_name']

class Conference_Area(models.Model):
    conf_id = models.ForeignKey(Conference, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)

    def __str__(self):
        return u"%s %s"%(self.conf_name, self.area_name)

    class Meta:
        db_table = 'conference_area'
        verbose_name = '会议-领域信息'
        verbose_name_plural = '会议-领域信息'
        ordering = ['area', 'conf_id']

class User_Institution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ins = models.ForeignKey(Institution, on_delete=models.CASCADE)

    def __str__(self):
        return self.user + " " + self.ins

    class Meta:
        db_table = 'user_institution'
        verbose_name = '用户关注学校'
        verbose_name_plural = '用户关注学校信息'
        ordering = ["user", 'ins']

class User_Conference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conf = models.ForeignKey(Conference, on_delete=models.CASCADE)

    def __str__(self):
        return self.user + " " + self.conf

    class Meta:
        db_table = 'user_conference'
        verbose_name = '用户关注会议'
        verbose_name_plural = '用户关注会议信息'
        ordering = ["user", 'conf']

class User_Area(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)

    def __str__(self):
        return self.user + " " + self.area

    class Meta:
        db_table = 'user_area'
        verbose_name = '用户关注领域'
        verbose_name_plural = '用户关注领域信息'
        ordering = ["user", 'area']

class User_Scholar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sch = models.ForeignKey(Scholar, on_delete=models.CASCADE)
    new_paper = models.BooleanField(default=False)

    def __str__(self):
        return self.user + " " + self.sch

    class Meta:
        db_table = 'user_scholar'
        verbose_name = '用户关注学者'
        verbose_name_plural = '用户关注学者信息'
        ordering = ["user", 'sch']
		
class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'note'
        verbose_name = '论文笔记'
        verbose_name_plural = '论文笔记'
        ordering = ['title']
		
class Remark(models.Model):
    content = models.TextField()
    date = models.DateField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return self.note+self.author

    class Meta:
        db_table = 'remark'
        verbose_name = '笔记评论'
        verbose_name_plural = '笔记评论'
        ordering = ['content']