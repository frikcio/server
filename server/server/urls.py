from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include("boards.urls")),
    path('', include("accounts.urls")),
    path('admin/', admin.site.urls),
]
