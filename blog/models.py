from django.db import models

#   모델 변경하면 마이그레이션하기 !!!

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

    #   제목에 포스트 번호와 제목 보여주기
    def __str__(self):
        return f'[{self.pk}] {self.title}'

    def get_absolute_url(self):  # 문자열은 f''로 넘김 / 고유 URL 부여하기

        return f'/blog/{self.pk}/'
