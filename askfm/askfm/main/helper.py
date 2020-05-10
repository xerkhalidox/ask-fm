from django.contrib.auth import get_user_model

class helper_methods:
    def condition_checker(self,string,threshold1,threshold2):
        if(len(string)>=threshold1 and len(string)<threshold2):
            return True
        else:
            return False
    def error_messages(self,error_code):
        error={
            'username_not_unique':'This username is used, Please choose another one',
            'username_length':'Username is too small or large, min length is 6 and max is 20',
            'email_not_unique':'This email is used, Please choose another one',
            'name_length':'Name is too small or large, min length is 6 and max is 20',
            'password_length':'Password is too small or large, min length is 6 and max is 20',
        }
        return error[error_code]
    def is_unique(self,field,data):
        user=get_user_model()
        if(field=='email'):
            if(user.objects.filter(email=data).count()==0):
                return True
            else:
                return False
        else:
            if(user.objects.filter(username=data).count()==0):
                return True
            else:
                return False
    def get_errors(self,request):
        errors=[]
        check=self.is_unique('email',request.POST["email"])
        if(not check):
            errors.append(self.error_messages('email_not_unique'))
        check=self.is_unique('username',request.POST["username"])
        if(not check):
            errors.append(self.error_messages('username_not_unique'))
        check=self.condition_checker(request.POST["name"],6,20)
        if(not check):
            errors.append(self.error_messages('name_length'))
        check=self.condition_checker(request.POST["username"],6,20)
        if(not check):
            errors.append(self.error_messages('username_length'))
        check=self.condition_checker(request.POST["password"],6,20)
        if(not check):
            errors.append(self.error_messages('password_length'))
        return errors
        


