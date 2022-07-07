from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np
from itertools import chain
from collections import Counter
import googletrans
from googletrans import Translator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.express as px
import matplotlib
import matplotlib.pyplot as plt
# %matplotlib inline
import re


# def load_insta():

#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

#     # specify the path to chromedriver.exe (download and save on your computer)
#     # open the webpage
#     driver.get("http://www.instagram.com")
#     return driver


def open_insta():

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("http://www.instagram.com")

    # target username
    username = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

    # enter username and password
    username.clear()
    username.send_keys("dhyani2250")
    password.clear()
    password.send_keys("Fx@2022")

    # time.sleep(2)
    # target the login button and click it
    button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[type='submit']"))).click()

    time.sleep(2)

    alert = WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
        (By.XPATH, '//button[contains(text(), "Not now")]'))).click()
    alert2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[class='_a9-- _a9_1']"))).click()

    return driver


def search_tag(driver=None, keyword=None):
    # target the search input field
    searchbox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
    searchbox.clear()

    # search for the hashtag
    keyword = keyword
    searchbox.send_keys(keyword)
    time.sleep(2)
    searchbox.send_keys(Keys.ENTER)
    searchbox.send_keys(Keys.ENTER)

    hashtag_url = 'https://www.instagram.com/explore/tags/'+keyword[1:]+'/'
    driver.get(hashtag_url)

    return hashtag_url, keyword

def get_totalposts(driver):
    soup_1 = BeautifulSoup(driver.page_source, "html.parser")
    total_post = soup_1.find('header').find('span').text
    total_post
    return total_post


def scroll(driver):
    time.sleep(1)
    SCROLL_PAUSE_TIME = 5
    post_urls = []
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        fetch_urls = driver.find_elements_by_xpath("//a[@href]")
        for url in fetch_urls:
            post_urls.append(url.get_attribute("href"))
        new_url = []
        for url in post_urls:
            if url.startswith('https://www.instagram.com/p/') and url not in new_url:
                new_url.append(url)
        # print(len(new_url))
        if len(new_url) >= 30:
            break
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    return new_url


def get_username(soup):
    # time.sleep(2)
    username = soup.find('header').find('span').text
    if len(username) == 0:
        username = soup.find('header').findAll('span')
        username = (username[1].text)
        if len(username) == 0:
            username = soup.find('header').findAll('span')
            username = (username[2].text)
    # print("username part---",username,'\n')
    return username


def get_likes(no_like, like, view, df):

    for l in like:
        for j in no_like:
            # print(j)
            if j.text == "Be the first to like this":
                # print(j.text)
                df["Likes/Views"] = "0 like"
        try:
            if l.text.endswith("like") and l.text.startswith("#") == False:
                df["Likes/Views"] = l.text
        except:
            pass
        if l.text.endswith("likes") and l.text.startswith("#") == False:
            df["Likes/Views"] = l.text
        elif not l.text.endswith("likes"):
            for v in view:
                try:
                    try:
                        if v.text.startswith("#"):
                            v.text = False
                    except:
                        pass
                    if v.text.endswith("views"):
                        df["Likes/Views"] = v.text
                except:
                    pass
    print("Likes part---", df["Likes/Views"], "\n")
    return df["Likes/Views"]


def get_mentions(mention):
    # time.sleep(1)
    mentions = []
    for m in mention:
        if m.text.startswith("@"):
            mentions.append(m.text)
        # else:
        #     if len(mentions) == 0:
        #         mentions = np.nan
    # df["Mentions"] = mentions
    # if len(df["Mentions"]) == 0:
    #     df["Mentions"] = np.nan
    # print("Mention part---",df["Mentions"],"\n")
    return mentions


def get_hashtags(hashtag):
    # time.sleep(1)
    hashtags = []
    for h in hashtag:
        if h.text.startswith("#"):
            hashtags.append(h.text)
    # print("hash part---",hashtags,"\n")
    return hashtags


def get_date(soup):
    # time.sleep(1)
    created = soup.find(
        'div', {'class': '_aacl _aacm _aacu _aacy _aad6'}).find('time').text
    # print("time part---",created,"\n")
    return created


def get_caption(driver, df):
    # time.sleep(2)
    soup_any = BeautifulSoup(driver.page_source, "html.parser")
    try:
        for i in soup_any.find('ul').findAll('a'):
            i.decompose()
        cap = soup_any.find('ul').findAll('span')
        try:
            text = "Verified"
            for j in cap:
                if (j.string == text):
                    j.decompose()
                    # print("this is loop j",j)
        except:
            pass

        df["Caption"] = (cap[1].text)
        # print("This is 1-----",df["Caption"])

        if len(cap[1]) == 0:
            df['Caption'] = (cap[2].text)
            # print('This is 2-------',df['Caption'])
            if len(cap[2]) == 0:
                df['Caption'] = (cap[3].text)
                # print('This is 3-------',df['Caption'])
    except:

        try:
            for i in soup_any.findAll('ul')[1].findAll('a'):
                i.decompose()
            cap_2 = soup_any.findAll('ul')[1].findAll('span')

            df["Caption"] = (cap_2[1].text)
            # print('This is 4------',df["Caption"])
            if len(cap_2[1]) == 0:
                # caption_new_2[2].text
                df['Caption'] = (cap_2[2].text)
                # print("this is part 5---",df['caps'])
        except:
            pass
    # print("Caption part---",df["Caption"], "\n")
    return df["Caption"]


def get_parameters(driver, url):

    df = {}
    # time.sleep(3)
    driver.get(url)
    time.sleep(3.5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    anchor = soup.findAll('a')
    anchor2 = soup.findAll('div')
    view = soup.findAll('section')

    try:
        df["URL"] = url
        df["Username"] = get_username(soup)
        try:
            df["Likes/Views"] = get_likes(anchor2, anchor, view, df)
        except:
            pass
            df["Likes/Views"] = '0 likes'
        df["Mentions"] = get_mentions(anchor)
        df["Hashtags"] = get_hashtags(anchor)
        df["Created At"] = get_date(soup)
        df["Caption"] = get_caption(driver, df)
    except:
        pass

    return df, anchor


def get_all(list1, driver, keyword):

    rel_hashtags = []
    mention_tag = []
    c = 0
    for url in list1:
        df, anchor = get_parameters(driver, url)

        try:
            rel_hashtags.append(get_hashtags(anchor))
        except:
            pass

        try:
            mentions = get_mentions(anchor)
            mention_tag.append(mentions)
        except:
            pass

        captions_value = []
        try:
            captions_value.append(df["Caption"])
        except:
            pass

        translator = Translator()
        translated_sentance = []
        # print('this part is list caption value---------',captions_value)
        for i in captions_value:
            print('THIS IS ORIGINAL CAPTIONS-------', i, '\n')

            df['language'] = None
            try:
                langs = translator.detect(i)
                print("Language name here", langs.lang)
                all_lang = googletrans.LANGUAGES
                if type(langs.lang) == str:
                    df['language'] = all_lang[langs.lang]                    
                    print("This is str", df['language'])

                else:
                    lang_list = []
                    for j in langs.lang:
                        lang_list.append(all_lang[j])
                        # print('This is list only',lang_list)
                        df['language'] = lang_list
                    print("This is list", df['language'])
                if not 'language' in df:
                    df['language'] = np.nan
                print(df["language"])
            except:
                pass
            if df['language'] == None:
                df['language'] = np.nan


            try:
                translation = translator.translate(i)
                translated_sentance.append(translation.text)
                analyzer = SentimentIntensityAnalyzer()
                df["translate caption"] = translated_sentance
            except:
                pass

            for s in translated_sentance:
                print("This is s text------->")
                vs = analyzer.polarity_scores(s)

            if vs['compound'] >= 0.05:
                print(s, '\n', vs, '\n', 'Positive', '\n')
                df['analysis'] = 'Positive'

            elif vs['compound'] <= -0.05:
                print(s, '\n', vs, '\n', 'Negative', '\n')
                df['analysis'] = 'Negative'

            else:
                print(s, '\n', vs, '\n', 'Natural', '\n')
                df['analysis'] = 'Neutral'

            data = pd.DataFrame([df])
            if c == 0:
                data.to_csv(keyword[1:]+' testing-07.csv',mode='a', sep=",", index=False, header=True)
                c += 1
            else:
                data.to_csv(keyword[1:]+' testing-07.csv',mode='a', sep=",", index=False, header=False)

    # new_data =  pd.read_csv(keyword[1:]+' testing.csv')
    # new_data['related_hash'] = pd.Series(common_hash)
    # new_data.to_csv(keyword[1:]+'Fianl.csv', mode='a', sep=',', index=False)
    #         print('%s: %d' % (tag, count))
    return rel_hashtags, mention_tag


def get_common(keyword, hash=None, mention=None):
    try:
        related_tag = []
        rel_hash = chain.from_iterable(hash)
        # print('this is only tags--------------------',hash)
        hash_count = Counter(rel_hash)
        for letter in hash_count.most_common(16):
            if letter[0] != keyword[0:]:
                related_tag.append(letter)
        print('This is common hash \n', *related_tag, sep='\n')
        return related_tag
    except:
        pass

    mention_list = []
    rel_menti = chain.from_iterable(mention)
    # print('this is only tags--------------------',mention)
    ment_count = Counter(rel_menti)
    for letter in ment_count.most_common(16):
        if letter[0] != keyword[0:]:
            mention_list.append(letter)
    print('This is common mention \n', *mention_list, sep='\n')

    return mention_list


#  load csv
data = pd.read_csv("photography testing-28.csv")
data

def get_langchart():
    # Language charrt
    x = data['language'].value_counts()
    # x.plot.bar()
    dic = x.to_dict()

    data1 = pd.DataFrame(dic, columns=['languages', 'counts'])
    data1['languages'] = dic.keys()
    data1['counts'] = dic.values()
    import plotly.express as px
    pie_chart = px.pie(data1, values='counts', names='languages',hover_name='languages',title='Languages in the captions',
                        template='plotly_dark',width=900,height=550, hole = 0.6)
    pie_chart.update_traces(textinfo='percent+label',textposition = 'inside',pull=[0.1],marker = dict(line = dict(color='cyan',width = 1)))
    pie_chart.show()

def split_it(likes):
        return int("".join(re.findall('\d+', likes)))

like_count = data["Likes/Views"]
filter_like = like_count.apply(split_it)
like_sum = filter_like.sum()


def get_tagdetail():
    # Likes bar chart
    
    time_period = int(input('How many posts data you want to see? :'))
    df_date_like = pd.DataFrame()
    like_view = data["Likes/Views"].head(time_period)
    like_new = like_view.apply(split_it)

    df_date_like["like"] = like_new
    df_date_like["like/view"] = data["Likes/Views"].head(time_period)
    df_date_like["date"] = data["Created At"].head(time_period)
    df_date_like["username"] = data['Username'].head(time_period)
    df_date_like["sentiment"] = data["analysis"].head(time_period)
    df_date_like["languages"] = data["language"].head(time_period)
    # df_date_like
    new_plot = px.bar(df_date_like,
                        x="date",
                        y="like",
                        hover_data=['sentiment'],
                        color="like/view",
                        hover_name='username',
                        labels={'date': 'Date, Time', 'like':'Numbers of Likes'},
                        text="username",
                        template='plotly_dark',
                        title="Likes chart based on posts",)
    new_plot.update_traces(width=0.6, opacity=0.7)
    new_plot.show()

def get_usercount():
    # user frequency chart
    x_user = data["Username"].value_counts().to_dict()
    df_user_analysis = pd.DataFrame()
    df_user_analysis["user_name"] = x_user.keys()
    df_user_analysis["user_freq"] = x_user.values()
    # df_user_analysis["check_like"] = data["Likes/Views"]
    df_user_analysis["time/date"] = data["Created At"]
    # df_user_analysis
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
    new_plot_user_analysis.show()

def get_OneUserDetails():
    # analysis on one user data
    one_user_data = data[data['Username'] == input("Enter Username :")]
    convert = one_user_data["Likes/Views"]
    one_user_data["like_num"] = convert.apply(split_it)
    # one_user_data
    plot_one_user_analysis = px.bar(one_user_data,
                        x="Created At",
                        y="like_num",
                        hover_data=['analysis','language'],
                        color="Likes/Views",
                        hover_name='Username',
                        labels={'Created At': 'Date/Time', 'like_num':'Numbers of likes'},
                        text="Likes/Views",
                        template='plotly_dark',
                        title="Showing the only one user data.")
    plot_one_user_analysis.update_traces(width=0.6, opacity=0.7)
    plot_one_user_analysis.show()

def get_TagSentiment():
    # sentiment chart
    sentiment = data["analysis"].value_counts().to_dict()
    df_sentiment_analysis = pd.DataFrame()
    df_sentiment_analysis["sentiment"] = sentiment.keys()
    df_sentiment_analysis["sentiment_freq"] = sentiment.values()
    # df_sentiment_analysis

    plot_sentimen_analysis = px.bar(df_sentiment_analysis,
                        x="sentiment",
                        y="sentiment_freq",
                        # hover_data=['analysis','language'],
                        color="sentiment",
                        # hover_name='Username',
                        # labels={'sentiment': '', 'sentiment_freq':'Numbers of likes'},
                        # text="Likes/Views",
                        template='plotly_dark',
                        title="Showing the sentiments of the all posts.")
    plot_sentimen_analysis.update_traces(width=0.6, opacity=0.7)
    plot_sentimen_analysis.show()

def get_RelatedHashtag():
    # wordcloud
    text = data['Hashtags'].tolist()
    text = ' '.join(text).lower()
    from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
    from PIL import Image

    wordcloud = WordCloud(width=1000,height=500,colormap='gist_rainbow_r', scale=5,prefer_horizontal=0.50,max_words=400,
                        collocations=True, background_color='black',relative_scaling=0.7).generate(text)
    # plot the wordcloud object
    plt.figure(figsize=(13,8), facecolor='k')
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig('Related_Hash.png', dpi = 300)
    plt.show()