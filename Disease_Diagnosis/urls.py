from django.urls import path
from . import views,views_flask

urlpatterns = [
    path('app-users/<int:user_id>', views.UserInfoView.as_view()),
    path('app-users', views.AllUserInfoView.as_view()),
    path('history', views.HistoryRecordView.as_view()),
    path('history/<int:pk>', views.SingleHistoryRecordView.as_view()),
    path('current-user', views.CurrentUserIdView.as_view(), name='current-user'),
    path('predict_chat',views_flask.get_chat_response),
    path('classify_image',views_flask.process_image)

]