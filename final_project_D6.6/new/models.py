from typing import List, Tuple
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce



#класс автор, связан с user
class Author(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.title()

#функция обновления рейтинга Автора
    def update_rating(self):
        author_post_rating = Post.objects.filter(author_id = self.pk).aggregate(r_p = Coalesce(Sum('rating'), 0))['r_p']
        author_com_rating = Comment.objects.filter(user_id = self.user).aggregate(r_c = Coalesce(Sum('rating'), 0))['r_c']
        author_post_com_rating = Comment.objects.filter(post__author__user = self.user).aggregate(r_pc = Coalesce(Sum('rating'), 0))['r_pc']

        self.rating = author_post_rating*3 + author_com_rating + author_post_com_rating
        self.save()


# класс категория
class Category(models.Model):
    name = models.CharField(max_length=150, unique= True)

    def __str__(self):
        return self.name.title()


#класс Постов, с указанием, какие посты бывают
class Post(models.Model):

    article = "AR"
    news = "PS"

    POSITION = [
        (article,'статья'),
        (news,'новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POSITION, default=news)
    post_time = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category)
    title = models.CharField(max_length=200)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title.title()}: {self.content[:20]}'

#функция like, dislike счетчик
    def like(self):
        self.rating += 1
        self.save()
    def dislike(self):
        self.rating -= 1
        self.save()

# Предварительный просмотр поста, вызывается отдельно, по запросу
    def preview(self):
        return self.content[0:124] + '...'


# класс связи: многие-ко-многим
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT, verbose_name= 'Пост')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')


#класс коментарии
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    com_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.title()}: {self.content[:20]}'

# функция like, dislike счетчик

    def like(self):
        self.rating += 1
        self.save()
    def dislike(self):
        self.rating -= 1
        self.save()

