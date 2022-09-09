# from email import message
import email
from django.contrib import messages
# from xxlimited import new
from django.shortcuts import render
from .operation import *
# from django.http import HttpResponse,response
from django.shortcuts import render,HttpResponseRedirect,Http404,redirect
# from rest_framework.parsers import JSONParser
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
# from django.template import loader
from django.contrib.auth.models import User,auth
from django.core.mail import send_mail
import math, random

# from .models import ItemsModel
# from .serializers import ItemSerializer

# def index(request):
   
#     result = request.data
#     # return render(request, 'result.html', {'result':result})

#     return Response("Hello world!",result)

def generateOTP() :
    digits = "0123456789"
    OTP = ""
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

@csrf_exempt
def send_otp(request):
    if request.method == "POST":
    
        useremail=request.POST.get("useremail")
        print(useremail)
        if User.objects.filter(email=useremail).first():
            messages.error(request,'Email is already taken')
            print("This Email is already has been taken")
            return redirect("login")
        else:
            o=generateOTP()
            htmlgen = '<p>Your OTP is <strong>'+o+'</strong></p>'
            send_mail('OTP request',o,'peterjenim23@gmail.com',[useremail],fail_silently=False,html_message=htmlgen)
            # print(o)
            # send_mail(
            # subject=f"OTP request :{o}",
            # message="hi nikhil!!!!",
            # from_email='peterjenim23@gmail.com',
            # recipient_list=[email],
            # fail_silently=False,
            # )
            return HttpResponse(o)
    else:
        return render(request, "auth-signup-basic.html")

@csrf_exempt
def handlesignup(request):
    if request.method == "POST":
        firstname = request.POST.get("first_name")
        lastname = request.POST.get("last_name")
        username = request.POST.get("user_name")
        useremail = request.POST.get("user_email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request,'Username is already taken')
            print("This Username is already has been taken")
            return redirect("signup")
        elif User.objects.filter(email=useremail).exists():
            messages.error(request,'Email is already taken')
            return redirect("signup")
        else:
            myuser = User.objects.create_user(username=username, password=password, email=useremail,first_name=firstname, last_name=lastname)
            # email=useremail,
            myuser.save()
            messages.success(request,"your account has been created successfully")
            return redirect("login")
    else:
        return render(request, "auth-signup-basic.html")

@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST.get('user_name')
        password = request.POST.get("pass_word")
        
        user = auth.authenticate(username = username, password = password)
        
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.error(request,"Please enter valid Username and Password")
            return redirect("login")
    else:
        return render(request,'auth-signin-basic.html')

def send_reset_pass_otp(request):
    if request.method == "POST":
        print("Here")
        useremail=request.POST.get("user_mail")
        print(useremail)
        if User.objects.filter(email=useremail).exists():
            o=generateOTP()
            request.session['Sent_Otp'] = o
            print(request.session['Sent_Otp'])
            htmlgen = '<p>Your OTP is <strong>'+o+'</strong></p>'
            send_mail('OTP request',o,'peterjenim23@gmail.com',[useremail],fail_silently=False,html_message=htmlgen)
            # print(o)
            # send_mail(
            # subject=f"OTP request :{o}",
            # message="hi nikhil!!!!",
            # from_email='peterjenim23@gmail.com',
            # recipient_list=[email],
            # fail_silently=False,
            # )
            return HttpResponse(o)            
        else:
            messages.error(request,'enter valid email!')
            print("Not receive valid email!")
            return redirect("forget")
    else:
        return render(request, "auth-pass-reset-basic.html")

def forget_pass(request):
    if request.method == "POST":
        useremail = request.POST.get('user_mail')
        request.session["user_mail"]=useremail
        print("This is forget pass usermail------------> ",useremail)
        if User.objects.filter(email=useremail).exists():
            send = send_reset_pass_otp(request)
            # send=send
            return redirect("confirm-otp")
        else:
            messages.error(request,'enter valid email!')
            print("Not receive valid email!")
            return redirect("forget")
    else:
        return render(request,'auth-pass-reset-basic.html')

def confirm_otp(request):
    if request.method == "POST":
        sent_otp = request.session['Sent_Otp']
        print(sent_otp)
        entered_otp = request.POST.get('OTP')
        print(entered_otp)
        if entered_otp == sent_otp:
            return redirect('pass-confirm')
        else:
            messages.error(request,'enter valid OTP!')
            return redirect('confirm-otp')
    return render(request,'enter-otp.html')

def confirm_pass(request):
    if request.method == "POST":
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if pass1==pass2:
            useremail=request.session["user_mail"]
            u=User.objects.get(email=useremail)
            if u:    
                u.set_password(pass1)
                u.save()
                return redirect('login')
            else:
                messages.error(request,'enter same password')            
                return redirect('pass-confirm')
        else:
            messages.error(request,'Please enter same password')            
            return redirect('pass-confirm')
    return render(request,'auth-pass-change-basic.html')


@csrf_exempt
def home(request):    
    return render(request,'pages-starter.html')

@csrf_exempt
def logout(request):
    auth.logout(request)
    
    return render(request,'auth-logout-basic.html')

@csrf_exempt
def about_us(request):    
    return render(request,'about-us.html')

@csrf_exempt
def contact_us(request):    
    return render(request,'contact-us.html')


@login_required(login_url="login")
@csrf_exempt
def index(request):

    # data = JSONParser().parse(request)
    # k=data['hastag']
    # print(data)
    searched_word = ''
    if request.method == "POST":
        searched_word = request.POST.get('search_keyword')
        print(searched_word)
    # # k="#sunday"
    # # data = JSONParser().parse(request)
    # # k=data['hastag']
    driver=open_insta()

    hashtag_url, keyword = search_tag(driver=driver, keyword=searched_word)

    driver.get(hashtag_url)
    print(hashtag_url)
    new_url = scroll(driver)
    print(len(new_url))
    total_post = get_totalposts(driver)
    print(total_post)
    ttl_post=total_post

    rel_hashtags,mention_tag = get_all(new_url,driver,keyword)
    related_tag = get_common(keyword ,rel_hashtags)
    mention_list = get_common(keyword ,mention_tag)
    print(related_tag, mention_list)
    # keyword = '#photo'
    data = read_csv(keyword)
    like_sum = total_like(data)
    lang, freq = get_langchart(data=data)
    chart_likes = get_tagdetail(data=data)
    user_name,user_count,df_user_analysis = get_usercount(data)
    user_detail_dic = get_OneUserDetails(data,df_user_analysis)
    user_detail_dic_2 = get_OneUserDetails_02(data,df_user_analysis)
    user_detail_dic_3 = get_OneUserDetails_03(data,df_user_analysis)
    user_detail_dic_4 = get_OneUserDetails_04(data,df_user_analysis)
    user_detail_dic_5 = get_OneUserDetails_05(data,df_user_analysis)
    # get_TagSentiment(data=data)
    get_RelatedHashtag(data=data)
    # chart=get_plotly_TagSentiment(data=data)
        

    sentiment = data["analysis"].value_counts().to_dict()
    new_list = []
    for i,j in sentiment.items():
        dict={"name":i, "data":[j]}
        new_list.append(dict)
    # print("This is modified list",new_list)
    # new_list_json = json.dumps(new_list, indent=4)
    # with open("/home/fxdata/Downloads/insta/vscode for insta/Folder for one file/Hastag/static/js/pages/new_list.js", "w+") as outfile:
    #     outfile.write(new_list_json)

    user = data["Username"].value_counts().to_dict()
    user_freq_data = []
    for i,j in user.items():
        dict_2 = {"name":i, "data":[j]}
        user_freq_data.append(dict_2)

    hash_name,hash_count = show_common_hash(data)  

    # ttl_post = '6535924'
    # searched_word = '#photo'
    # print(user_detail_dic_3)
    d={"post":ttl_post,"hashtag":searched_word[1:], "likes":like_sum,"chart_likes":chart_likes,'new_list': new_list,'lang':lang,
    'freq':freq, 'user_name':user_name[:15],'user_count':user_count[:15],'one_user_data':user_detail_dic,'one_user_data_2':user_detail_dic_2,
    'one_user_data_3':user_detail_dic_3,'one_user_data_4':user_detail_dic_4,'one_user_data_5':user_detail_dic_5,'hash_name1':hash_name[1],
    'hash_count1':hash_count[1],'hash_name2':hash_name[2],'hash_count2':hash_count[2],'hash_name3':hash_name[3],'hash_count3':hash_count[3],
    'hash_name4':hash_name[4],'hash_count4':hash_count[4],'hash_name5':hash_name[5],'hash_count5':hash_count[5],'hash_name6':hash_name[6],
    'hash_count6':hash_count[6],'hash_name7':hash_name[7],'hash_count7':hash_count[7],'hash_name8':hash_name[8],'hash_count8':hash_count[8],
    'hash_name9':hash_name[9],'hash_count9':hash_count[9],'hash_name10':hash_name[10],'hash_count10':hash_count[10],'hash_name11':hash_name[11],
    'hash_count11':hash_count[11],'hash_name12':hash_name[12],'hash_count12':hash_count[12],'hash_name13':hash_name[13],'hash_count13':hash_count[13],
    'hash_name14':hash_name[14],'hash_count14':hash_count[14],'hash_name15':hash_name[15],'hash_count15':hash_count[15]}
    # 'hash_name1':hash_name[0],
    # 'hash_count1':hash_count[0]

    # return HttpResponse("id")
    return render(request, "dashboard-crm.html", d)


# def testing(request):
#   template = loader.get_template('template.html')
#   c = {
#     'var1': 'John\nDoe',
#   }
#   return render(request, "template.html", c)
#   return HttpResponse(template.render(context, request))