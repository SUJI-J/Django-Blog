from django.db import models
from django.contrib.auth.models import User
import os

#   모델 변경하면 마이그레이션하기 !!!
#   카테고리에서 똑같이 따오셈
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # 문자열은 f''로 넘김 / 고유 URL 부여하기
        return f'/blog/category/{self.slug}/'

    class Meta:
        verbose_name_plural = 'Categories'
        #   화면 상에 보여지는 이름 설정


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    content = models.TextField()

    #   헤드 이미지랑 파일 업로드 만들기
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d', blank=True)

    #   자동으로 작성시각과 수정시각 저장하기
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #   on_delete = models.CASCADE 작성자 지우면 게시글도 지워짐 / blank=False니까 무조건 선택 해야됨
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    #   선택 안 해도 됨
    #   One To Many 관계
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    #   Many to Many 관계 - 자동으로 null됨
    tags = models.ManyToManyField(Tag, blank=True)

    #   제목에 포스트 번호와 제목 보여주기
    def __str__(self):
        return f'[{self.pk}] {self.title}   ::  {self.author}'

    def get_absolute_url(self):  # 문자열은 f''로 넘김 / 고유 URL 부여하기
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]
        # [-1] => 맨 뒤에 있는 확장자가 됨

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField() # 사용자가 작성하는 것은 이것 뿐
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'
        # 댓글들, detail에서도 고유 번호를 부여하도록 함
