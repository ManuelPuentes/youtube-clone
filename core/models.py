from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(unique=True, null=False)
    two_factor_auth = models.CharField(
        max_length=50,
        blank=True,
        unique=True,
        null=True,
        verbose_name="Código 2FA",
        db_column='2fa'
    )

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="customuser_set",  # or 'core_customuser_groups'
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",  # or 'core_customuser_permissions'
        related_query_name="customuser",
    )

    USERNAME_FIELD = 'email'  # Campo usado para el login
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    class Meta:
        db_table = 'custom_user'
        verbose_name = "Usuario Personalizado"
        default_related_name = 'custom_users'
        verbose_name_plural = "Usuarios Personalizados"
        # Ordenar por fecha de creación descendente
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Actualiza automáticamente updated_at al guardar
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)


class Video(models.Model):
    # este es el id del video
    id = models.CharField(max_length=20, primary_key=True, unique=True, error_messages={
        'unique': "Ya existe un video con este embed URL"
    })
    title = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=1000, null=False)
    thumbnail = models.URLField(null=False)
    duration = models.CharField(null=False, default='PT5M')
    upload_date = models.DateTimeField(default=timezone.now)
    uploader = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    @property
    def total_likes(self):
        return self.likes.filter(like_dislike=True).count()

    @property
    def total_dislikes(self):
        return self.likes.filter(like_dislike=False).count()
    

    @property
    def comments(self):
        return self.comments.all()


class Vote(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE,  related_name='likes')
    like_dislike = models.BooleanField()  # True for like, False for dislike

    class Meta:
        # One like/dislike per user per video
        unique_together = ('user', 'video')


class Comment(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE,  related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}: {self.text[:50]}"
