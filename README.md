# ask-fm
Ask.fm is a social networking site where users create profiles and can send each other questions. It was once a form of anonymous social media that encouraged questions to be submitted anonymously.
## Table of contents
* [Dependencies](#dependencies)
* [Getting started](#getting-started)
* [Project status](#project-status)

## Dependencies
* Django >= 2.2
* pymysql
## Getting started
Clone the project using this command
~~~ 
git clone https://github.com/xerkhalidox/ask-fm.git
~~~
and go to settings.py file and configure database to your credentials 
~~~
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'askfm',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
    }
}
~~~
then run
~~~
cd askfm/askfm
~~~
then run
~~~
py manage.py makemigrations
~~~
then run 
~~~
py manage.py migrate
~~~
then run the server by
~~~
py manage.py runserver
~~~
and open  localhost:8000 on your browser 

## Project features and status
- [x] User can register and login to his account.
- [x] User can ask each others anonymously or being identified.
- [x] Users can follow or unfollow each others.
- [x] Users can get list of his friends.
- [x] Users have feed page to see recent answers of his friends.
- [x] User will be notified when another user asks him or an answer he has asked was answered.
  
