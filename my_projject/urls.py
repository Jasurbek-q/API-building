
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken import views as auth_views
from jobs import views as job_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/api-token-auth/', auth_views.obtain_auth_token, name='api_token_auth'),
    path('api/jobs/', job_views.VacancyCreateAPIView.as_callable()
    if hasattr(job_views.VacancyCreateAPIView, 'as_callable') else job_views.VacancyCreateAPIView.as_view(), name='vacancy-list'),
    path('api/jobs/<int:pk>/', job_views.VacancyDetailAPIView.as_view(), name='vacancy_detail'),
    path('api/jobs/<int:pk>/', job_views.VacancyDetailAPIView.as_callable()
    if hasattr(job_views.VacancyDetailAPIView, 'as_callable') else job_views.VacancyDetailAPIView.as_view(), name='vacancy-detail'),
]
