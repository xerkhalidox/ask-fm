from django.urls import path
from . import views

urlpatterns = [
    path("", views.landpage_handler.as_view(), name="landpage"),
    path("login", views.landpage_handler.as_view(), name="login"),
    path("signup", views.landpage_handler.as_view(), name="signup"),
    path("register", views.register, name="register"),
    path("auth", views.login_user, name="auth"),
    path("<str:username>/", views.homepage, name="homepage"),
    path("logout", views.logout_user, name="logout"),
    path("<str:username>/ask", views.question_asked, name="question_asked"),
    path("account/questions", views.question_list, name="question_list"),
    path(
        "account/questions/delete/<int:question_id>",
        views.delete_question,
        name="delete_question",
    ),
    path("<str:username>/follow", views.follow_user, name="follow_user"),
    path("<str:username>/unfollow", views.unfollow_user, name="unfollow_user"),
    path("friends", views.get_friends, name="friends"),
    path("notifications", views.get_notifications, name="notifications"),
    path(
        "account/question/answer/<int:question_id>",
        views.answer_question.as_view(),
        name="answer_question",
    ),
    path("account/home", views.user_home, name="userhome"),
]
