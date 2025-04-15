from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    class Roles(models.TextChoices):
        CANDIDATE = 'candidate', 'Candidate'
        HR = 'hr', 'HR Manager'
        ADMIN = 'admin', 'Administrator'

    email = models.EmailField(unique=True)
    patronymic = models.CharField(max_length=50, blank=True, null=True) # добавил отчество, имя и фамилия есть в AbstractUser, если не будем делать
                                                                         # кастомную модель юзера
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.CANDIDATE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    resumefile = models.FileField(upload_to='resumes/', null=True)
    resumetext = models.CharField(max_length=3000, blank=True)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class Vacancy(models.Model):
    class EmploymentType(models.TextChoices):
        FULL_TIME = 'full_time', 'Full Time'
        PART_TIME = 'part_time', 'Part Time'
        INTERN = 'intern', 'Internship'
        CONTRACT = 'contract', 'Contract' #пока накидал базово

    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.JSONField()
    responsibilities = models.JSONField()
    location = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=20, choices=EmploymentType.choices)
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'hr'})


class Application(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'New'
        REVIEWING = 'reviewing', 'Reviewing'
        INTERVIEW = 'interview', 'Interview'
        REJECTED = 'rejected', 'Rejected'
        ACCEPTED = 'accepted', 'Accepted'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    resume = models.ForeignKey(Resume, on_delete=models.SET_NULL, null=True)
    text = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)


class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/', null=True, blank=True) # это надо настроить, но пока чтобы было
    published_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'hr'})


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.IntegerField() # пока просто интежером, базово
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)


class ContactRequest(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'New'
        HANDLED = 'handled', 'Handled' # не знаю надо или нет, типо ответка на реквест

    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)