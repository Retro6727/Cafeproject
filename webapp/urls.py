from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.show, name='home'),
    path('category/<int:id>/', views.cat_view, name='category'),
    path('product/<int:id>/', views.cat_view, name='product'),
    path('addprod/<int:id>/',views.addprod,name="addprod"),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('ty/', views.tym, name='thanks'),
    path('range/', views.range, name='range'),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)