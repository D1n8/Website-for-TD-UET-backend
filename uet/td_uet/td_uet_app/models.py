from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# Упростить, уберём регистрацию, оставить чисто для админа/HR (Дима)

# с юзерами надо переделывать, так как рассчитывал на регистрацию, но скорее всего обойдусь чисто Permissions AllowAny, посмотрим (02.05 - Дима)
class User(AbstractUser):
    class Roles(models.TextChoices):
        CANDIDATE = 'candidate', 'Candidate'
        HR = 'hr', 'HR Manager'
        ADMIN = 'admin', 'Administrator'

    email = models.EmailField(unique=True)
    patronymic = models.CharField(max_length=50, blank=True, null=True) 
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.CANDIDATE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Vacancy(models.Model):
    class EmploymentType(models.TextChoices):
        FULL_TIME = 'full_time', 'Full Time'
        PART_TIME = 'part_time', 'Part Time'
        INTERN = 'intern', 'Internship'
        CONTRACT = 'contract', 'Contract'

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

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"

    def __str__(self):
        return self.title


# Отдельные модели резюме скорее всего не нужны? (02.05 - Дима) 

# class Resume(models.Model):
#     resumefile = models.FileField(upload_to='resumes/', null=True)
#     resumetext = models.CharField(max_length=3000, blank=True)
#     title = models.CharField(max_length=100)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name = "Резюме"
#         verbose_name_plural = "Резюме"

#     def __str__(self):
#         return self.title
    

class Application(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'New'
        REVIEWING = 'reviewing', 'Reviewing'
        INTERVIEW = 'interview', 'Interview'
        REJECTED = 'rejected', 'Rejected'
        ACCEPTED = 'accepted', 'Accepted'

    #новая форма, так как юзер - анон
    surname = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    #модель резюме пока перенесена сюда (02.05 - Дима) 
    resume_file = models.FileField(upload_to='resumes/')
    resume_text = models.TextField()
    text = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Отклик"
        verbose_name_plural = "Отклики"

    def __str__(self):
        return self.user


class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/', null=True, blank=True) # это надо настроить, но пока чтобы было
    published_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'admin'})

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title


# тут не знаю, как делать отзывы с анонимными пользователями (02.05 - Дима)
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.IntegerField() # пока просто интежером, базово
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return self.user

class ContactRequest(models.Model):

    surname = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return self.name