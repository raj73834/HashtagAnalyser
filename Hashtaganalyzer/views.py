from django.shortcuts import render
from .operation import *
from django.http import HttpResponse,response
from django.shortcuts import render,HttpResponseRedirect,Http404
from rest_framework.parsers import JSONParser
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from .models import ItemsModel
# from .serializers import ItemSerializer

# def index(request):
   
#     result = request.data
#     # return render(request, 'result.html', {'result':result})

#     return Response("Hello world!",result)

@csrf_exempt
def index(request):

    # data = JSONParser().parse(request)
    # k=data['hastag']
    k="#moj"
    # data = JSONParser().parse(request)
    # k=data['hastag']
    driver=open_insta()

    hashtag_url, keyword = search_tag(driver=driver, keyword=k)

    driver.get(hashtag_url)
    print(hashtag_url)
    new_url = scroll(driver)
    print(len(new_url))
    total_post = get_totalposts(driver)
    print(total_post)
    ttl_post=total_post
    like_sum
    rel_hashtags,mention_tag = get_all(new_url,driver,keyword)
    related_tag = get_common(keyword ,rel_hashtags)
    mention_list = get_common(keyword ,mention_tag)
    print(related_tag, mention_list)

    get_langchart()
    get_tagdetail()
    # get_usercount()
    # get_OneUserDetails()
    get_TagSentiment()
    get_RelatedHashtag()
    
  
    d={"post":ttl_post,"hashtag":k, "likes":like_sum}

    # return HttpResponse("id")
    return render(request, "dashboard-crm.html", d)