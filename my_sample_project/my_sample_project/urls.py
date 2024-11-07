
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("home_app.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
    path ('' ,include('blog_app.urls')),
]
