from django.contrib import admin
from django.contrib.auth import views as auth_views
from iris_classifier import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from iris_classifier.views import IrisViewSet

# API Router
router = DefaultRouter()
router.register(r'iris', IrisViewSet)

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', views.home_view, name='home'),
    
    # Authentication Views
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    
    # CRUD Views
    path('create/', views.iris_create, name='iris_create'),
    path('update/<int:pk>/', views.iris_update, name='iris_update'),
    path('delete/<int:pk>/', views.iris_delete, name='iris_delete'),
    
    # Search and Data Operations
    path('search/', views.iris_search, name='search'),
    path('export/', views.export_iris_csv, name='export_csv'),
    path('import/', views.import_iris_csv, name='import_csv'),

    # Password Reset Views
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='password_reset.html'), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), 
         name='password_reset_complete'),

    # AI View
    path('predict/', views.predict_view, name='predict'),

    # API View
    path('api/', include(router.urls)), # API adresimiz: http://127.0.0.1:8000/api/iris/
]

from django.conf import settings
from django.conf.urls.static import static


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])