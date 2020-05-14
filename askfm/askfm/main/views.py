from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .models import Question, Follow, Answer, Question_Notification, Answer_Notification
from . import helper


def homepage(request, username):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/")
    User = get_object_or_404(get_user_model(), username=username)
    is_followed = Follow.objects.filter(user=User, follower=request.user)
    if len(is_followed) < 1:
        is_followed = False
    else:
        is_followed = True
    answers = Answer.objects.filter(user=User)
    return render(
        request,
        "main/homepage.html",
        {"User": User, "is_followed": is_followed,
            "answers": reversed(answers)},
    )


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")


class landpage_handler(TemplateView):
    def get(self, request):
        if not request.user.is_authenticated:
            template_name = request.path_info
            if request.path_info == "/":
                template_name = "landpage"
            template = loader.get_template("main/" + template_name + ".html")
            return HttpResponse(template.render({}, request))
        else:
            return HttpResponseRedirect("/" + request.user.username)


def login_user(request):
    if request.method == "GET":
        return HttpResponseRedirect("/" + request.user.username)
    user = authenticate(
        username=request.POST["username"], password=request.POST["password"]
    )
    if user is not None:
        login(request, user)
        return HttpResponseRedirect("/" + request.user.username)
    else:
        return HttpResponseRedirect("/login")


def register(request):
    if request.method == "GET":
        return HttpResponseRedirect("/" + request.user.username)
    errors = helper.helper_methods().get_errors(request)
    if len(errors) != 0:
        messages.error(request, "Email or username is already taken")
        return HttpResponseRedirect("/signup")
    user = get_user_model()
    user.objects.create_user(
        email=request.POST["email"],
        password=request.POST["password"],
        username=request.POST["username"],
        name=request.POST["name"],
        gender=request.POST["gender"],
    ).save()
    user = authenticate(
        username=request.POST["username"], password=request.POST["password"]
    )
    login(request, user)
    return HttpResponseRedirect("/" + request.POST["username"])


def question_asked(request, username):
    unknown = request.POST.get("anon", False)
    if unknown == "on":
        unknown = True
    else:
        unknown = False
    user_asks = get_object_or_404(
        get_user_model(), username=request.user.username)
    user_asked = get_object_or_404(get_user_model(), username=username)
    que = Question(
        question=request.POST["question"],
        is_anon=unknown,
        is_answered=0,
        user_asks=user_asks,
        user_asked=user_asked,
    )
    que.save()
    new_notification = Question_Notification(
        user=user_asked,
        question=que,
        is_read=0
    )
    new_notification.save()
    return HttpResponseRedirect("/" + username)


def question_list(request):
    user = request.user
    ques = Question.objects.all().filter(user_asked_id=user.id, is_answered=0)
    que_counts = len(ques)
    return render(request, "main/question.html", {"ques": ques, "count": que_counts})


def delete_question(request, question_id):
    Question.objects.filter(pk=question_id).delete()
    return HttpResponseRedirect(reverse("question_list"))


def follow_user(request, username):
    followed = get_object_or_404(get_user_model(), username=username)
    follow_relationship = Follow(user=followed, follower=request.user)
    follow_relationship.save()
    return HttpResponseRedirect(reverse("homepage", args=(username,)))


def unfollow_user(request, username):
    User = get_object_or_404(get_user_model(), username=username)
    Follow.objects.filter(user=User, follower=request.user).delete()
    return HttpResponseRedirect(reverse("homepage", args=(username,)))


def get_friends(request):
    user = request.user
    friends = Follow.objects.filter(follower=user)
    return render(request, "main/friends.html", {"friends": friends})


def get_notifications(request):
    question_notifications=Question_Notification.objects.filter(user=request.user)
    answer_notifications=Answer_Notification.objects.filter(user=request.user)
    context={"questions":question_notifications,"answers":answer_notifications}
    for notification in question_notifications:
        notification.is_read=1
        notification.save()
    for notification in answer_notifications:
        notification.is_read=1
        notification.save()
    return render(request, "main/notifications.html",context)


class answer_question(TemplateView):
    def get(self, request, question_id):
        question = Question.objects.get(id=question_id)
        return render(request, "main/answer.html", {"question": question})

    def post(self, request, question_id):
        answer = request.POST["answer"]
        question = Question.objects.get(id=question_id)
        question.is_answered = 1
        question.save()
        new_answer = Answer(
            answer=answer, question=question, user=request.user)
        new_answer.save()
        new_notification = Answer_Notification(
            user=question.user_asks,
            answer=new_answer,
            is_read=0
        )
        new_notification.save()
        return HttpResponseRedirect(reverse("homepage", args=(request.user,)), {"notification": 1})


def user_home(request):
    friends = Follow.objects.filter(follower=request.user)
    users = [friend.user for friend in friends]
    users.append(request.user)
    answers = Answer.objects.filter(user__in=users)
    response = render(request, "main/userhome.html",
                      {"answers": reversed(answers)})
    response.http_test = 1
    return response
