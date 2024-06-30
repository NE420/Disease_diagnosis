from django.urls import path
from . import views,views_flask

urlpatterns = [
    path('app-users', views.UserInfoView.as_view()),#Used for GET and PUT operations for user info
    path('app-users/createInfo',views.UserInfoCreateView.as_view()),#Used To create a new userinfo
    path('app-users/all', views.AllUserInfoView.as_view()),
    path('history', views.HistoryRecordView.as_view()),
    path('history/<int:pk>', views.SingleHistoryRecordView.as_view()),
    path('predict_chat',views_flask.get_chat_response),
    path('classify_image',views_flask.process_image)

]