from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Chat, Messages
from .utils import retrieve_data, rerank_documents, generate_answer, answer
from django.contrib.auth.models import User
from .serializers import ChatSerializer, MessageSerializer
from rest_framework import status
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.
class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('chat-list')
        return render(request, 'register.html', {'form': form})
    
class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('chat-list')
            else:
                messages.error(request, "Invalid username or password.")
        return render(request, 'login.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class AskView(APIView):
    def get(self, request):
        return render(request, 'ask.html')
    def post(self, request):
        user = request.user
        
        question_text = request.data.get("question", "")
        title = request.data.get("title", "Untitled Chat")
        
        if not question_text:
            return Response({"error": "Câu hỏi không được để trống"}, status=status.HTTP_400_BAD_REQUEST)
        chat = Chat.objects.create(user=user, title=title)
        
        question_message = Messages.objects.create(
            chat = chat,
            message_type = "question",
            content = question_text
        )
        
        try:
            answer_text = answer(question_text)
        except Exception as e:
            return Response({"error": f"Đã xảy ra lỗi khi tạo câu trả lời: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        answer_message = Messages.objects.create(
            chat = chat,
            message_type = "answer",
            content = answer_text
        )
        
        return Response({
            "chat_id": chat.id,
            "question": question_text,
            "answer": answer_text
        }, status=status.HTTP_201_CREATED)

@method_decorator(login_required, name='dispatch')
class ChatListView(APIView):
    def get(self, request):
        chats = Chat.objects.filter(user=request.user).select_related('user').order_by('created_at')
        chat_serializer = ChatSerializer(chats, many=True)
        return Response(chat_serializer.data, status=status.HTTP_200_OK)

@method_decorator(login_required, name='dispatch')
class ChatDetailView(APIView):
    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id, user=request.user)
            message = Messages.objects.filter(chat=chat).order_by('created_at')
            message_serializer = MessageSerializer(message, many=True)
            return Response(message_serializer.data, status=status.HTTP_200_OK)
        except Chat.DoesNotExist:
            return Response({"error": "Chat not found"}, status=status.HTTP_404_NOT_FOUND)
