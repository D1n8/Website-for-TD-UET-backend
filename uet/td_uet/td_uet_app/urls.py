from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ResumeViewSet, VacancyViewSet, ApplicationViewSet, NewsViewSet, ReviewViewSet, ContactRequestViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'resumes', ResumeViewSet)
router.register(r'vacancies', VacancyViewSet)
router.register(r'applications', ApplicationViewSet)
router.register(r'news', NewsViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'contact-requests', ContactRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]