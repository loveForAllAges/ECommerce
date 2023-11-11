from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Chat, Message
from account.models import User
from django.db.models import Q
from django.views import View,generic
from rest_framework import views, response, status
from .serializers import ChatSerializer
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import Http404
from django.db.models import Count


class StaffOnly(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self) -> bool | None:
        if self.request.user.is_staff or self.request.user.is_superuser:
            return True
        raise Http404
    

class ChatList(StaffOnly, ListView):
    template_name = 'admin_chat.html'
    queryset = Chat.objects.annotate(num_messages=Count('messages')).filter(num_messages__gt=0).order_by('-created_at')


class AgentList(StaffOnly, ListView):
    template_name = 'agent-list.html'

    def get_queryset(self):
        return User.objects.filter(Q(is_staff=True) | Q(is_superuser=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chat_name'] = self.request.session.session_key
        return context


class ChatAPIView(views.APIView):
    def post(self, request):
        sk = request.session.session_key

        if sk:
            if request.user.is_authenticated:
                data, trash = Chat.objects.get_or_create(client=request.user)
            else:
                data, trash = Chat.objects.get_or_create(sk=sk)
        else:
            request.session['chat'] = []
            request.session.save()
            sk = request.session.session_key
            data = Chat.objects.create(sk=sk)

        serializer = ChatSerializer(data)
        return response.Response(serializer.data)


class ChatClose(StaffOnly, View):
    def post(self, request):
        pk = request.POST.get('chat_id', None)
        chat = get_object_or_404(Chat, pk=pk, agent=request.user)
        chat.agent = None
        chat.status = 3
        chat.save()
        return redirect('chat-detail', pk)


# class ActivateChatAPIView(StaffOnly, views.APIView):
#     def post(self, request):
#         try:
#             chat = Chat.objects.get(pk=request.data['chat_id'], agent__isnull=True)
#             chat.agent = request.user
#             chat.status = 1
#             chat.save()
#             data = ChatSerializer(chat).data
#             st = status.HTTP_200_OK
#         except:
#             data = dict()
#             st = status.HTTP_404_NOT_FOUND

#         return response.Response(data, status=st)


# class ActivateChatAPIView(StaffOnly, View):
#     def post(self,request):
#         pk = request.data['chat_id']
#         print(pk)
#         chat = get_object_or_404(Chat, pk=pk, agent__isnull=True)
#         chat.agent = request.user
#         chat.status = 1
#         chat.save()

#         return redirect('chat-detail', pk)
