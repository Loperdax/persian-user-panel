from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# First go to MyUser() class read and comeback to MyUserManager()
# اول برین کلاس MyUser() رو ببینین تا با فیلد های یوزر آشنا شین و بعدش برگردین به این MyUserManager()

# This class is a manager for user and superuser
# با استفاده از این منیجر میتونین یوزر و یا سوپریوزر (ادمین) بسازین
class MyUserManager(BaseUserManager):
    
    # This function is used to create a normal user. (Same as normal site user)
    # این تابع برا ساخت یوزر معمولی یا همون کاربر سایت استفاده میشه که برای ورودی :
    # email , password , first_name , last_name میخواد
    def create_user(self, email, password=None, **extra_fields):
        
        # Raises an error when the email is not set
        # ایمیل به صورت ضروری در میاد و درصورت ست نشدن ارور میده
        if not email:
            raise ValueError('Email must be set')
        
        # Normalize_email is a classmethode in "BaseUserManager" that will normalize email
        # ایمیلو نرمالایز میکنیم تا به فرمت استاندارد جنگو در بیاد 
        # example@GMAIL.com -> example@GMAIL.com
        email = self.normalize_email(email)
        
        # Create a user model with given extrafields
        # یک یوزر را با اطلاعات اضافه ای (مثل وضعیت و ...) که وارد کردیم می سازیم
        user = self.model(email=email, **extra_fields)
        # User now is an object from "BaseManager.model" class and has a classmethode :  set_password() for set password
        # یوزر ما در حال حاضر یک آبجکت از "BaseManager.model" هس که برای خودش کلاس متد های مخصوص خودشو داره 
        # مثل set_password() که یه پسوورد رو به یوزر اختصاص میده. پسورد باید به ورودی تابع داده شه
        user.set_password(password)
        
        # And save it in db
        # مدل یوزر رو سیو می کنیم یا به عبارتی تو دیتابیس ذخیرش می کنیم
        user.save()
        
        # And return it
        # و برش می گردونیم
        return user
    
    # This function is used to create a super user or admin
    # این تابع برای ساخت سوپر یوزر یا ادمین استفاده میشه 
    # کارشم اینه فقد یه مقدار رو عوض میکنه و یکی دیگرو اضافه میکنه در نهایت بازم تابع بالایی فراخونی میشه
    def create_superuser(self, email, password=None, **extra_fields):
        
        # We can access the extrafields that are sent and give default values to the parameters
        # برای ساخت سوپر یوزر باید تعیین کنیم که اول این یوزر کارمند سایت باشد (یعنی یوزر عادی نباشد)
        # و همچنین با تغییر مقدار is_superuser به True این یوزر را به عنوان ادمین میشناسیم
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        
        # Another way:  یه راه دیگ:           -----> founded in django user model 
        # extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_superuser', True)
        
        # Finally, the above function is called
        # در آخر وقتی مقادیر تغییر کرد تابع create_user فراخونی میشه
        return self.create_user(email, password, **extra_fields)
    
    
    # A function to change user profile , It is possible to put conditions regarding the changed value
    # for example, when the email is changed, the 'email_validation' will be false and the email needs to be confirmed again.
    # این تابع برای تغییر مشخصات کاربر بکار میره میشه توش شرط هایی هم نسبت به مقدار تغییر کرده گذاشت
    # مثلا وقتی ایمیل تغییر کرد کانفیرمیشن  فالس شه و دوباره نیاز به تایید ایمیل داشته باشه
    def edit_user(self, user, **extra_fields):
        for field, value in extra_fields.items():
            # if field == 'email' :
            #     setattr(user, 'email_validation', False)
            setattr(user, field, value)
            
            # if field be password hash it 
            # اگه این کارو نمی کردیم پسورد بصورت تکس سیو می شد. ولی الان مثل بالا بصورت hash شده سیو میشه
            if field == 'password':
                user.set_password(value)
        user.save()
        return user

    
    
# This is a user model that inherits from AbstractBaseUser
# این یک مدل یوزره که از AbstractBaseUser ارث بری کرده
class MyUser(AbstractBaseUser):
    
    # The first field is an EmailField that has its own validations. 
    # We also set unique to true so that emails are unique, that is, no email is used for two users
    # فیلد اول برای ایمیله که اومدیم از models.EmailField استفاده کردیم که برای خودش ولیدیشن های خودشو داره تا ایمیل درست وارد شه
    # همچینین unique را true قرار دادیم تا بصورت منحصر به فرد باشه و هر ایمیل فقط برا یه یوزر استفاده شه
    email = models.EmailField(unique=True)
    
    # First name and last name use models.CharField, the maximum length of which should be 30 characters
    #نام و نام خانوادگی از models.CharField استفاده می کنن که حداکثر طول اونا باید ۳۰ کارکتر باشه 
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    
    # These two items are models.BooleanField and can be True or False
    # Which are used to determine the activeness and status of the employee, etc.
    # این دو مورد از نوع models.BooleanField هستند و میتونن True و یا False باشند که برای تعیین فعال بودن و وضعیت کارمند و... استفاده میشن.
    # is_staff بعدا برای تعیین دسترسی استفاده میشه و جدا کننده یوزر های معمولی و یوزر های دارای دسترسیه
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # It entrusts the management of this model to a model named MyUserManager
    # Which can be used in views and other places.
    # مدیریت این مدل رو به یه مدل دیگ به اسم MyUserManager میسپاره که میشه از اون مدیر تو view  ها و جاهای دیگ استفاده کرد
    objects = MyUserManager()

    # Determining the desired field for user input.
    # میاد میگ کدوم فیلد برای ورود کاربر استفاده شه
    USERNAME_FIELD = 'email'
    
    # As the name suggests, to determine the required fields
    # همانطور که از اسمش پیداس برای تعیین فیلدای مورد نیازه . اینجا علاوه بر ایمیل و پسورد نام و نام خانوادگی هم اجباریه
    # REQUIRED_FIELDS = ['first_name', 'last_name']

    # When we printed our model it will show the email . it also use in django admin panel
    # این تابع برا وقتیه که مدلمونو پرینت کردیم بیاد ایمیل رو نمایش بده
    def __str__(self):
        return self.email

    # a function that return full name
    # یه تابع نوشتیم که اگ اسم کامل یه مدلو خواستیم بده
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    # a function that return firstname
    # همچینین یه تابع دیگ درست کردیم تا اسم خالیو بده
    def get_short_name(self):
        return self.first_name
