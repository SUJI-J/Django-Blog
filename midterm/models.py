from django.db import models

# Create your models here.
class Staff(models.Model):
    code = models.CharField(max_length=15)
    name = models.CharField(max_length=30)
    Rank = models.CharField(max_length=100)
    image = models.ImageField(upload_to='midterm/images/%Y/%m/%d', blank=True)

    def __str__(self):
        return f'{self.name} [{self.Rank}]'

    def get_absolute_url(self):  # 문자열은 f''로 넘김 / 고유 URL 부여하기
        return f'/midterm/list/{self.pk}/'

    def get_absolute_url2(self):
        return f'/midterm/list/{self.pk}/alter/'