from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect , HttpResponse


# This view is used for user login
# این view برای لاگین شدن یوزر استفاده می شود 
def login_view(request):
    
    # This condition checks the type of request, if it is a post, it checks the input information to log in the user if it is correct.
    # This login can be checked later with a variable
    # این شرط میاد نوع ریکوئست رو بررسی میکنه که اگ post بود بیاد اطلاعات ورودی رو چک کنه 
    # و در صورت درست بودن یوزر رو لاگین کنه . این لاگین شدن رو میشه با یه متغیر بررسی کرد.
    if request.method == 'POST':
        
        #get 'email' and 'password' attribute
        # مقدار email و پسورد رو که از طریق فرم html ارسال شده رو دریافت می کنه
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # the authenticate func checking information    if it's correct 'user' will be our user model object from db
        #این فانکشن اطلاعات ورودی رو چک می کنه و در صورت صحیح بودن یک ابجکت از مدل یوزر ما بر می گردونه
        # در غیر این صورت none بر میگرداند
        user = authenticate(request, email=email, password=password)
        if user is not None:
            
            # checking user status -> active or not
            if user.is_active:
                
                # logged in
                login(request, user)
                return  HttpResponse('Logged in')
        else:
            return render(request, 'login.html', {'error_message': 'Wrong email or password'})
    
    # if request methode isn't POST 
    # اگر متد ما post نبود صفحه لاگین رندر شه
    else:
        return render(request, 'login.html')
    

