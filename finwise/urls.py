from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('register.urls')),
    path('stocks/', include('stocks.urls')),
    path('chats/', include('chat.urls'))
]
