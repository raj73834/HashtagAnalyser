from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
from pyvirtualdisplay import Display
import pandas as pd
import numpy as np
from itertools import chain
from collections import Counter
import googletrans
from googletrans import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.express as px
import matplotlib.pyplot as plt
# %matplotlib inline
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
import re
import os
import httpx
import json
from urllib.parse import quote
from typing import Optional


# def load_insta():

#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

#     # specify the path to chromedriver.exe (download and save on your computer)
#     # open the webpage
#     driver.get("http://www.instagram.com")
#     return driver


def scrape_hashtag(hashtag: str, session: httpx.AsyncClient, page_size=12, page_limit:Optional[int] = None):
    """scrape user's post data"""
    base_url = "https://www.instagram.com/graphql/query/?query_hash=298b92c8d7cad703f7565aa892ede943&variables="
    variables = {
        "tag_name": hashtag,
        "first": page_size,
        "after": None,
    }
    page = 1
    # print(base_url + quote(json.dumps(variables)))
    while True:
        result = session.get(base_url + quote(json.dumps(variables)))
        print(result)
        hashtag_count = json.loads(result.content)['data']['hashtag']['edge_hashtag_to_media']['count']
        yield hashtag_count
        posts = json.loads(result.content)["data"]["hashtag"]["edge_hashtag_to_media"]
        # print(posts)
        for post in posts['edges']:
            yield post["node"]
        page_info = posts["page_info"]
        if not page_info["has_next_page"]:
            break
        variables["after"] = page_info["end_cursor"]
        page += 1

def scrape_hashtag_data(keyword=None):
    scrolled_posts = []
    keyword = keyword
    with httpx.Client(timeout=httpx.Timeout(20.0),) as session:
        for user in scrape_hashtag(hashtag=keyword, session=session):
            # print(user)
            scrolled_posts.append(user)
            if (len(scrolled_posts)>=800):
                break
            if (len(scrolled_posts) >= 500 and len(scrolled_posts) <= 510):
                print("Wait time is called")
                time.sleep(15)
            # if (len(scrolled_posts) >= 600 and len(scrolled_posts) <= 610):
            #     print("Wait time is called-2")
            #     time.sleep(10)
            # break
    return scrolled_posts, keyword

def for_url(scrolled_posts):
    final_url = []
    for i in range(len(scrolled_posts)):
        # print(i)
        if type(scrolled_posts[i]) == dict:
            data_scroll = scrolled_posts[i].get('shortcode')
            # print(data_scroll)
            final_url.append("https://www.instagram.com/p/"+data_scroll)
        # final_url = set(final_url)
    return final_url

def for_like(scrolled_posts):
    like = []
    for i in range(len(scrolled_posts)):
        # print(i)
        if type(scrolled_posts[i]) == dict:
            data_like = scrolled_posts[i].get('edge_liked_by').get('count')
            # print(data_like)
            like.append(data_like)
    return like

def for_username(scrolled_posts):
    import instaloader
    load = instaloader.Instaloader()

    username = []
    for i in range(len(scrolled_posts)):
        data_userid = scrolled_posts[i].get('owner').get('id')
        data_username = instaloader.Profile.from_id(load.context,data_userid)
        print(data_username.username)
        username.append(data_username.username)
    return username

def for_time(scrolled_posts):
    import time
    import datetime
    post_time = []
    for i in range(len(scrolled_posts)):
        # print(i)
        if type(scrolled_posts[i]) == dict:
            data_timestamp = scrolled_posts[i].get('taken_at_timestamp')
            timestamp = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(data_timestamp))
            post_time.append(timestamp)
            # print(timestamp)
    return post_time

def for_hashtag_mention(scrolled_posts):
    import re
    hashtag = []
    mentions = []
    # clean_captions = []
    for i in range(len(scrolled_posts)):
        if type(scrolled_posts[i]) == dict:
            # print(i)
            # '#[a-z0-9_]+'
            #'(\w+)'
            try:
                data_caption = scrolled_posts[i].get('edge_media_to_caption').get('edges')[0].get('node').get('text')
                filtered = re.findall('#(\w+)', data_caption)
                # for hash_filter in filtered:
                hashtag.append(filtered)
                mention = re.findall('(@[a-zA-Z0-9_]{1,50})', data_caption)
                mentions.append(mention)
            except IndexError:
                hashtag.append("no hashtags")
                mentions.append("no mentions")
            except Exception as e:
                print(e)
            
            # print(data_caption)

            # for iter in filtered:
            #     data_caption = data_caption.replace(iter, "")
            # for iter in mention:
            #     data_caption = data_caption.replace(iter, "")
            #     clean_captions.append(data_caption)
    return hashtag,mentions

def for_caption(scrolled_posts):
    import re,string

    def strip_links(text):
        link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
        links         = re.findall(link_regex, text)
        for link in links:
            text = text.replace(link[0], ', ')    
        return text

    def strip_all_entities(text):
        entity_prefixes = ['@','#']
        for separator in string.punctuation:
            if separator not in entity_prefixes :
                text = text.replace(separator,' ')
        words = []
        for word in text.split():
            word = word.strip()
            if word:
                if word[0] not in entity_prefixes:
                    words.append(word)
        return ' '.join(words)
    
    tests = []
    # try:
    for i in range(len(scrolled_posts)):
        # print(i)
        if type(scrolled_posts[i]) == dict:
            try:
                data_caption = scrolled_posts[i].get('edge_media_to_caption').get('edges')[0].get('node').get('text')
                tests.append(data_caption)
            except IndexError:
                tests.append("no caption")
                # print(tests)
            except Exception as e:
                print(e)
    # except:
    #     pass
    # tests = [
    #     "@peter I really love that shirt at #Macy. http://bet.ly//WjdiW4",
    #     "@shawn Titanic tragedy could have been prevented Economic Times: Telegraph.co.ukTitanic tragedy could have been preve... http://bet.ly/tuN2wx",
    #     "I am at Starbucks http://4sh.com/samqUI (7419 3rd ave, at 75th, Brooklyn)",
    # ]
    clean_captions = []
    for t in tests:
        clean_texts = strip_all_entities(strip_links(t))
        # print(clean_texts)
        clean_captions.append(clean_texts)
    return clean_captions

def make_dataframe(scrolled_posts):
    df = pd.DataFrame()
    df["Url"] = for_url(scrolled_posts)
    # df["Username"] = for_username()
    # df["Likes"] = for_like()
    df["Likes"] = for_like(scrolled_posts)
    hashtag,mentions = for_hashtag_mention(scrolled_posts)
    df["Mentions"] = (mentions)
    df["Hashtags"] = (hashtag)
    df["Created_at"] = for_time(scrolled_posts)
    df["Captions"] = (for_caption(scrolled_posts))
    return df

def translate_and_sentiment(df,keyword):
    dataframe = []
    translator = Translator()
    language = json.load(open("language.json"))
    for i,j in df.iterrows():
        # print(i,j)
        # print(len(j['Captions']))
        if len(j['Captions']) == 0:
            j['language'] = 'no caption'
        else:
            # j['langguage'] = 'english'
            # try:
            try:
                langs = translator.detect(j['Captions'])
                print("Language name here", langs.lang)
                all_lang = language
                # print("This is language full name",all_lang[langs.lang])
                if type(langs.lang) == str:
                    j['language'] = all_lang[langs.lang]
                    print("This is language full name",all_lang[langs.lang])
                else:
                    print("execution going into else part======")
                    lang_list = []
                    for l in langs.lang:                        
                        lang_list.append(all_lang[l])
                    print('This is multi language',lang_list)
                    j['language'] = (lang_list)
            except:
                pass
            translated_sentance = []
            try:
                translation = translator.translate(j['Captions'])
                translated_sentance.append(translation.text)
                # print(translation.text)
                analyzer = SentimentIntensityAnalyzer()
                j["translate caption"] = translation.text
            except:
                pass
            if len(j['Captions']) == 0:
                j['translate caption'] = 'No caption'

            for s in translated_sentance:
                # print("This is s text------->")
                vs = analyzer.polarity_scores(s)

                if vs['compound'] >= 0.05:
                    # print(s, '\n', vs, '\n', 'Positive', '\n')
                    j['analysis'] = 'Positive'
                elif vs['compound'] <= -0.05:
                    # print(s, '\n', vs, '\n', 'Negative', '\n')
                    j['analysis'] = 'Negative'
                else:
                    # print(s, '\n', vs, '\n', 'Natural', '\n')
                    j['analysis'] = 'Neutral'
        dataframe.append(j)
    final_df = pd.DataFrame(dataframe)
    final_df.to_csv(keyword+"_10-11_new_csv_structure_extra_clm.csv")
        # break
    return final_df



def read_csv(keyword = None):
    print("This is read_csv keyword------->",keyword)
    # load csv
    data = pd.read_csv(keyword+"_10-11_new_csv_structure_extra_clm.csv")
    return data

def get_langchart(data):
    # Language charrt
    x = data['language'].value_counts()
    # x.plot.bar()
    dic = x.to_dict()
    lang = list(dic.keys())
    freq = list(dic.values())

    data1 = pd.DataFrame(dic, columns=['languages', 'counts'])
    data1['languages'] = dic.keys()
    data1['counts'] = dic.values()
    import plotly.express as px
    pie_chart = px.pie(data1, values='counts', names='languages',hover_name='languages',title='Languages in the captions',
                        template='plotly_dark',width=900,height=550, hole = 0.6)
    pie_chart.update_traces(textinfo='percent+label',textposition = 'inside',pull=[0.1],marker = dict(line = dict(color='cyan',width = 1)))
    # pie_chart.show()

    return lang, freq

# def split_it(likes):
#     try:        
#         return int("".join(re.findall('\d+', likes)))
#     except:
#         pass

def total_like(data):
    like_count = data["Likes"]
    # filter_like = like_count
    like_sum = like_count.sum()
    return like_sum

def get_main_sentiment(data):
    show_sentiment = data['analysis'].value_counts().to_dict()
    show_sentiment
    main_sentiment = []
    for i in show_sentiment:
        # print(i)
        main_sentiment.append(i)
        break
    return main_sentiment

def get_tagdetail(data):
    # Likes bar chart
    
    # time_period = int(input('How many posts data you want to see? :'))
    df_date_like = pd.DataFrame()
    # like_view = data["Likes/Views"].head(time_period)
    like_view = data["Likes"]
    # like_new = like_view

    df_date_like["like"] = like_view
    df_date_like["like/view"] = like_view
    df_date_like["date"] = data["Created_at"]
    # df_date_like["username"] = data['Username']
    df_date_like["sentiment"] = data["analysis"]
    df_date_like["languages"] = data["language"]


    # df_for_apex =df_date_like['date'].to_list()
    # df_for_apex_2 =df_date_like['like'].to_list()

    # # likes_data = list(zip(df_for_apex, df_for_apex_2))
    # # likes_data
    # likes_data_dic = []
    # likes_data = list(zip(df_for_apex, df_for_apex_2))
    # # likes_data
    # for i in likes_data:
    #     # print(i)
    #     likes_data_make = {"name":i[0], "data":[i[1]]}
    #     # print(likes_data_make)
    #     likes_data_dic.append(likes_data_make)
    

    df_date_like
    new_plot = px.bar(df_date_like,
                        x="date",
                        y="like",
                        hover_data=['sentiment'],
                        color="like/view",
                        # hover_name='sentiment',
                        labels={'date': 'Date/Time', 'like':'Numbers of Likes'},
                        # text="username",
                        template='plotly_dark',
                        height=550,
                        title="Likes chart based on posts",)
    new_plot.update_traces(width=0.8, opacity=0.7)
    chart_likes = new_plot.to_html()

    return chart_likes

def get_usercount(data):
    # user frequency chart
    x_user = data["Username"].value_counts().to_dict()
    df_user_analysis = pd.DataFrame()
    df_user_analysis["user_name"] = x_user.keys()
    df_user_analysis["user_freq"] = x_user.values()
    # df_user_analysis["check_like"] = data["Likes/Views"]
    df_user_analysis["time/date"] = data["Created_at"]
    # df_user_analysis
    user_name = list(x_user.keys())
    user_count = list(x_user.values())


    new_plot_user_analysis = px.bar(df_user_analysis,
                                    x="user_name",
                                    y="user_freq",
                                    # hover_data=['time/date'],
                                    color="user_freq",
                                    hover_name='user_name',
                                    labels={'user_name': 'Name of the user', 'user_freq':'Numbers of users'},
                                    # text="username",
                                    template='plotly_dark',                                    
                                    title="Shown Which user are use # multiple time")
    new_plot_user_analysis.update_traces(width=0.6, opacity=0.7)
    # new_plot_user_analysis.show()

    return user_name,user_count,df_user_analysis

def get_OneUserDetails(data,df_user_analysis):
    stor = df_user_analysis["user_name"].to_list()
    one_user_data = data[data['Username'] == stor[0]]
    # one_user_data
    df_for_oneuser_data = pd.DataFrame(one_user_data)

    for_user_apex_0 = df_for_oneuser_data['Username'].to_list()
    for_user_apex_1 = df_for_oneuser_data['Created At'].to_list()
    for_user_apex_2 = df_for_oneuser_data['Likes/Views'].to_list()
    for_user_apex_3 = df_for_oneuser_data['analysis'].to_list()
    for_user_apex_4 = df_for_oneuser_data['language'].to_list()

    user_detail_dic = []
    user_data = list(zip(for_user_apex_0, for_user_apex_1,for_user_apex_2,for_user_apex_3,for_user_apex_4))
    for i in user_data:
        making_userdata = {"name":i[1],"data":[{'username':i[0],'x':i[1],'y':i[2],'sentiment':i[3],'language':i[4]}]}
        user_detail_dic.append(making_userdata)
    stor1 = stor[0]

    # plot_one_user_analysis = px.bar(one_user_data,
    #                     x="Created At",
    #                     y="like_num",
    #                     hover_data=['analysis','language'],
    #                     color="Likes/Views",
    #                     hover_name='Username',
    #                     labels={'Created At': 'Date/Time', 'like_num':'Numbers of likes'},
    #                     text="Likes/Views",
    #                     template='plotly_dark',
    #                     title="Showing the only one user data.")
    # plot_one_user_analysis.update_traces(width=0.6, opacity=0.7)
    # plot_one_user_analysis.show()

    return user_detail_dic,stor1

def get_OneUserDetails_02(data,df_user_analysis):
    stor = df_user_analysis["user_name"].to_list()
    one_user_data = data[data['Username'] == stor[1]]
    # one_user_data
    df_for_oneuser_data = pd.DataFrame(one_user_data)

    for_user_apex_0 = df_for_oneuser_data['Username'].to_list()
    for_user_apex_1 = df_for_oneuser_data['Created At'].to_list()
    for_user_apex_2 = df_for_oneuser_data['Likes/Views'].to_list()
    for_user_apex_3 = df_for_oneuser_data['analysis'].to_list()
    for_user_apex_4 = df_for_oneuser_data['language'].to_list()

    user_detail_dic_2 = []
    user_data = list(zip(for_user_apex_0, for_user_apex_1,for_user_apex_2,for_user_apex_3,for_user_apex_4))
    for i in user_data:
        making_userdata = {"name":i[1],"data":[{'username':i[0],'x':i[1],'y':i[2],'sentiment':i[3],'language':i[4]}]}
        user_detail_dic_2.append(making_userdata)
    stor2 = stor[1]

    return user_detail_dic_2,stor2

def get_OneUserDetails_03(data,df_user_analysis):
    stor = df_user_analysis["user_name"].to_list()
    one_user_data = data[data['Username'] == stor[2]]
    # one_user_data
    df_for_oneuser_data = pd.DataFrame(one_user_data)

    for_user_apex_0 = df_for_oneuser_data['Username'].to_list()
    for_user_apex_1 = df_for_oneuser_data['Created At'].to_list()
    for_user_apex_2 = df_for_oneuser_data['Likes/Views'].to_list()
    for_user_apex_3 = df_for_oneuser_data['analysis'].to_list()
    for_user_apex_4 = df_for_oneuser_data['language'].to_list()

    user_detail_dic_3 = []
    user_data = list(zip(for_user_apex_0, for_user_apex_1,for_user_apex_2,for_user_apex_3,for_user_apex_4))
    for i in user_data:
        making_userdata = {"name":i[1],"data":[{'username':i[0],'x':i[1],'y':i[2],'sentiment':i[3],'language':i[4]}]}
        user_detail_dic_3.append(making_userdata)
    stor3 = stor[2]
    return user_detail_dic_3,stor3

def get_OneUserDetails_04(data,df_user_analysis):
    stor = df_user_analysis["user_name"].to_list()
    one_user_data = data[data['Username'] == stor[3]]
    # one_user_data
    df_for_oneuser_data = pd.DataFrame(one_user_data)

    for_user_apex_0 = df_for_oneuser_data['Username'].to_list()
    for_user_apex_1 = df_for_oneuser_data['Created At'].to_list()
    for_user_apex_2 = df_for_oneuser_data['Likes/Views'].to_list()
    for_user_apex_3 = df_for_oneuser_data['analysis'].to_list()
    for_user_apex_4 = df_for_oneuser_data['language'].to_list()

    user_detail_dic_4 = []
    user_data = list(zip(for_user_apex_0, for_user_apex_1,for_user_apex_2,for_user_apex_3,for_user_apex_4))
    for i in user_data:
        making_userdata = {"name":i[1],"data":[{'username':i[0],'x':i[1],'y':i[2],'sentiment':i[3],'language':i[4]}]}
        user_detail_dic_4.append(making_userdata)
    stor4 = stor[3]
    return user_detail_dic_4,stor4

def get_OneUserDetails_05(data,df_user_analysis):
    stor = df_user_analysis["user_name"].to_list()
    one_user_data = data[data['Username'] == stor[4]]
    # one_user_data
    df_for_oneuser_data = pd.DataFrame(one_user_data)

    for_user_apex_0 = df_for_oneuser_data['Username'].to_list()
    for_user_apex_1 = df_for_oneuser_data['Created At'].to_list()
    for_user_apex_2 = df_for_oneuser_data['Likes/Views'].to_list()
    for_user_apex_3 = df_for_oneuser_data['analysis'].to_list()
    for_user_apex_4 = df_for_oneuser_data['language'].to_list()

    user_detail_dic_5 = []
    user_data = list(zip(for_user_apex_0, for_user_apex_1,for_user_apex_2,for_user_apex_3,for_user_apex_4))
    for i in user_data:
        making_userdata = {"name":i[1],"data":[{'username':i[0],'x':i[1],'y':i[2],'sentiment':i[3],'language':i[4]}]}
        user_detail_dic_5.append(making_userdata)
    stor5 = stor[4]

    return user_detail_dic_5,stor5

def get_TagSentiment(data):
    # sentiment chart
    sentiment = data["analysis"].value_counts().to_dict()
    df_sentiment_analysis = pd.DataFrame()
    df_sentiment_analysis["sentiment"] = sentiment.keys()
    df_sentiment_analysis["sentiment_freq"] = sentiment.values()
    # df_sentiment_analysis

    # plot_sentimen_analysis = px.bar(df_sentiment_analysis,
    #                     x="sentiment",
    #                     y="sentiment_freq",
    #                     # hover_data=['analysis','language'],
    #                     color="sentiment",
    #                     # hover_name='Username',
    #                     # labels={'sentiment': '', 'sentiment_freq':'Numbers of likes'},
    #                     # text="Likes/Views",
    #                     template='plotly_dark',
    #                     title="Showing the sentiments of the all posts.")
    # plot_sentimen_analysis.update_traces(width=0.6, opacity=0.7)
    # plot_sentimen_analysis.show()

def show_common_hash(data):
    hash_list = data["Hashtags"].to_list()
    color_list = ['text-primary','text-info','text-success','text-secondary','text-danger','text-warning']
    j=0
    look_common_hash = []
    for i in hash_list:
        look_common_hash.extend(eval(i))
    hash_name = []
    hash_count = []
    color_arr = []
    hash_cont = Counter(look_common_hash)
    # print(hash_conter)
    for letter, count in hash_cont.most_common(51):
        # if letter != keyword[0:]:
            # print(letter, count)
            hash_name.append(str(letter))
            hash_count.append(str(count))
            color_arr.append(color_list[j-1])
            if j==len(color_list):
                j=0
            else:
                j+=1
    return hash_name, hash_count,color_arr
   

#     return chart
def get_RelatedHashtag(data):
    # wordcloud
    text = data['Hashtags'].tolist()
    text = ' '.join(text).lower()
    # from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
    # from PIL import Image

    wordcloud = WordCloud(width=1000,height=580,colormap='gist_rainbow_r',prefer_horizontal=0.50,
                        collocations=True, background_color='black',relative_scaling=0.5).generate(text)
    # plot the wordcloud object
    # plt.figure(figsize=(13,8), facecolor='k')
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    # plt.tight_layout(pad=0)
    wordcloud.to_file('static/Related_Hash.png')
    # plt.savefig('static/Related_Hash.jpg',dpi = 500,bbox_inches = 'tight')    
    # plt.show()