from django.urls import path
from . import views

urlpatterns = [
    path('app-users/<int:user_id>', views.UserInfoView.as_view()),
    path('app-users', views.AllUserInfoView.as_view()),
    path('history', views.HistoryRecordView.as_view()),
    # path('history/<int:pk>', views.singleHistoryRecordView.as_view()),
    path('current-user', views.CurrentUserIdView.as_view(), name='current-user'),
]