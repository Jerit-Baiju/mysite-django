from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    log = models.TextField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Video(models.Model):
    video_file = models.FileField(upload_to='videos')
    yt = models.ForeignKey('YT_Video', on_delete=models.CASCADE)


class YT_Video(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class AdminLog(models.Model):
    name = models.CharField(max_length=40, null=True)
    latest_log = models.CharField(max_length=250, null=True, blank=True)
    log = models.TextField(null=True, blank=True)


class AdminSecret(models.Model):
    name = models.CharField(max_length=20, null=True)
    secret = models.CharField(max_length=100, null=True, blank=True)
