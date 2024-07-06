from django.urls import path
from . import views,views_flask
from .views import ChatSessionListCreateView, ChatSessionDetailView

urlpatterns = [
    path('app-users', views.UserInfoView.as_view()),#Used for GET and PUT operations for user info
    path('app-users/createInfo',views.UserInfoCreateView.as_view()),#Used To create a new userinfo
    path('app-users/all', views.AllUserInfoView.as_view()),
    path('predict_chat',views_flask.ProcessChatView.as_view()),
    path('classify_image',views_flask.ProcessImageView.as_view()),
    path('chat-sessions/', ChatSessionListCreateView.as_view()),
    path('chat-sessions/<int:pk>/', ChatSessionDetailView.as_view()),
    #path('interactions/', InteractionListCreateView.as_view()),

]