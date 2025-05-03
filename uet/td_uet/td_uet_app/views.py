from rest_framework import viewsets
from .models import User, Vacancy, Application, News, Review, ContactRequest
from .serializers import UserSerializer, VacancySerializer, ApplicationSerializer, NewsSerializer, ReviewSerializer, ContactRequestSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ContactRequestViewSet(viewsets.ModelViewSet):
    queryset = ContactRequest.objects.all()
    serializer_class = ContactRequestSerializer