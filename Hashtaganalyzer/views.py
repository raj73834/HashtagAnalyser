# from email import message
from django.contrib import messages
# from xxlimited import new
from django.shortcuts import render
from .operation import *
# from django.http import HttpResponse,response
from django.shortcuts import render,HttpResponseRedirect,Http404,redirect
# from rest_framework.parsers import JSONParser
# from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
# from django.template import loader
from django.contrib.auth.models import User,auth

# from .models import ItemsModel
# from .serializers import ItemSerializer

# def index(request):
   
#     result = request.data
#     # return render(request, 'result.html', {'result':result})

#     return Response("Hello world!",result)
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
            myuser = User.objects.create_user(username=username, password=password, email=useremail, first_name=firstname, last_name=lastname)
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


@login_required(login_url="login")
@csrf_exempt
def index(request):

    # data = JSONParser().parse(request)
    # k=data['hastag']
    # print(data)
    # searched_word = ''
    if request.method == "POST":
        searched_word = request.POST.get('search_keyword')
        print(searched_word)
    # k="#sunday"
    # data = JSONParser().parse(request)
    # k=data['hastag']
    driver=open_insta()

    hashtag_url, keyword = search_tag(driver=driver, keyword=searched_word)

    driver.get(hashtag_url)
    print(hashtag_url)
    new_url = scroll(driver)
    print(len(new_url))
    total_post = get_totalposts(driver)
    print(total_post)
    ttl_post=total_post

    # rel_hashtags,mention_tag = get_all(new_url,driver,keyword)
    # related_tag = get_common(keyword ,rel_hashtags)
    # mention_list = get_common(keyword ,mention_tag)
    # print(related_tag, mention_list)

    data = read_csv(keyword)
    like_sum = total_like(data)
    lang, freq = get_langchart(data=data)
    chart_likes = get_tagdetail(data=data)
    user_name,user_count,df_user_analysis = get_usercount(data)
    user_detail_dic = get_OneUserDetails(data,df_user_analysis)
    get_TagSentiment(data=data)
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

    # print(user_detail_dic)
    print("--------------post",type(ttl_post))
    print("-------------likes",type(like_sum))
    d={"post":ttl_post,"hashtag":searched_word[1:], "likes":like_sum,"chart_likes":chart_likes,'new_list': new_list,'lang':lang,
    'freq':freq, 'user_name':user_name[:15],'user_count':user_count[:15],'one_user_data':user_detail_dic}

    # return HttpResponse("id")
    return render(request, "dashboard-crm.html", d)


# def testing(request):
#   template = loader.get_template('template.html')
#   c = {
#     'var1': 'John\nDoe',
#   }
#   return render(request, "template.html", c)
#   return HttpResponse(template.render(context, request))