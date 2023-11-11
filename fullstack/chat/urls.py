from django.urls import path
from .views import *


urlpatterns = [
    path('get-chat-data/', ChatAPIView.as_view(), name='get-chat-data'),
    # path('activate/', ActivateChatAPIView.as_view(), name='chat-activate'),
    path('close/', ChatClose.as_view(), name='chat-close'),
]
