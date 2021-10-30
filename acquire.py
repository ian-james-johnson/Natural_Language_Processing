import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

import unicodedata
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords



def parse_gulde_news():
    """ 
    Returns a dataframe of scraped web-scraping-demo.zgulde.net/news 
    """
    url = 'https://web-scraping-demo.zgulde.net/news' # set the url
    # setting the agent so Codeup site doesn't block our web-scraper
    agent = 'codeup ds germain' 
    # query
    response = requests.get(url, headers={'User-Agent': agent})
    # soup, features argument is added to prevent a warning
    # if we don't have features argument, then soup will assume that we want the parser to be for lxml
    soup = BeautifulSoup(response.text, features="lxml") 
    # raw list of articles
    articles = soup.select('.grid.gap-y-12 > div') 
    # initialise list of dicts for dataframe
    article_list = [] 
    # parse each article
    for article in articles: 
        # grab title
        title = article.h2.text 
        # grab date, author, contents of article
        date, author, contents = article.select('.py-3')[0]\
            .find_all('p') 
        # add dict of info to list
        article_list.append({'title':title, 'date':date.text, 
            'author':author.text, 'contents':contents.text}) 
    return pd.DataFrame(article_list) # return dataframe

def parse_gulde_people():
    """ 
    Returns dataframe of scraped web-scraping-demo.zgulde.net/people 
    """
    # set the url
    url = 'https://web-scraping-demo.zgulde.net/people' 
    agent = 'codeup ds germain'
    # query
    response = requests.get(url, headers={'User-Agent': agent}) 
    # soup
    soup = BeautifulSoup(response.text, features="lxml") 
    # raw list of people
    people = soup.find_all('div', {'class':'person'}) 
    # initialise list of dicts for dataframe
    info_list = [] 
    # parse each person
    for person in people: 
        # grab name
        name = person.h2.text 
        # grab more info
        quote, email, phone, address = person.find_all('p') 
        # fix info
        quote, email, phone, address = quote.text.strip(), email.text, phone.text, address.text.strip()
        # set regex for address fix
        regexp = r'\s{2,}' 
        # fix address
        address = re.sub(regexp, ' ', address) 
        # create dict
        person_dict = {'name':name, 'quote':quote, 'email':email, 
                       'phone':phone, 'address':address} 
        # add dict to list
        info_list.append(person_dict) 

    # return dataframe
    return pd.DataFrame(info_list) 

def codeup_blog_urls():
    """ 
    Return list of URLs for codeup blogs for exercise 
    """
    url1 = 'https://codeup.com/data-science/codeups-data-science-career-accelerator-is-here/'
    url2 = 'https://codeup.com/data-science/data-science-myths/'
    url3 = 'https://codeup.com/data-science/data-science-vs-data-analytics-whats-the-difference/'
    url4 = 'https://codeup.com/data-science/10-tips-to-crush-it-at-the-sa-tech-job-fair/'
    url5 = 'https://codeup.com/data-science/competitor-bootcamps-are-closing-is-the-model-in-danger/'
    return [url1, url2, url3, url4, url5]

def acquire_codeup_blog(url):
    """ 
    Returns dict of one codeup blog's title, date, category, and content 
    """
    # set the agent
    agent = 'codeup ds germain'
    # query 
    response = requests.get(url, headers={'User-Agent': agent}) 
    # soup, added features argument to prevent warning
    soup = BeautifulSoup(response.text, features="lxml") 
    # get title
    title = soup.select('.entry-title')[0].text 
    # get date
    date = soup.select('.published')[0].text 
    # get category
    category = soup.find_all('a', {'rel':'category tag'})[0].text 
    # grab all unformatted paragraphs
    paragraphs = soup.find_all('div', {'class':'et_pb_module et_pb_post_content et_pb_post_content_0_tb_body'})[0]\
    .find_all('p')
    # create list for formatted paragraphs
    paragraph_list = [] 
    # iterate paragraphs
    for paragraph in paragraphs: 
        # add to list
        paragraph_list.append(paragraph.text) 

    # destroy href markers
    content = " ".join(paragraph_list).replace('\xa0', ' ') 
    # create dict
    blog_info_dict = {'title':title, 'date':date, 'category':category, 'content':content}
    # return dict
    return blog_info_dict

def get_blogs():
    """ 
    Queries, returns a dataframe of each codeup blog article's stuff 
    """
    # initialise the dictionary
    list_of_blog_dicts = [] 
    for url in codeup_blog_urls():
        # add each blog to the list of blogs dictionary
        list_of_blog_dicts.append(acquire_codeup_blog(url)) 
    return pd.DataFrame(list_of_blog_dicts)

def get_article(url):
    """ 
    Return dataframe of articles in inshorts category URL 
    """
    # set the agent
    agent = 'codeup ds germain' 
    # query
    response = requests.get(url, headers={'User-Agent': agent}) 
    # soup, added features argument to prevent warning
    soup = BeautifulSoup(response.text, features="lxml") 
    # get category
    category = soup.find_all('li', {'class':'active-category selected'})[0].text 
    # get raw cards
    cards = soup.select('.news-card') 
    # create list of dicts for dataframe
    card_dict_list = [] 
    # iterate each card
    for card in cards: 
        # headline
        headline = card.find_all('span', {'itemprop':'headline'})[0].text 
        # publish time
        publish_time = card.find_all('span', {'class':'time'})[0].text 
        # content
        content = card.find_all('div', {'itemprop':'articleBody'})[0].text.strip() 
        # create dict
        card_dict = {'headline':headline, 'publish_time':publish_time,
                       'category':category, 'content':content} 
        # push dict to list
        card_dict_list.append(card_dict) 
    # return dataframe
    return pd.DataFrame(card_dict_list) 

def inshorts_urls():
    """ 
    Return list of inshorts URLs for exercise 
    """
    url1 = 'https://inshorts.com/en/read/business'
    url2 = 'https://inshorts.com/en/read/sports'
    url3 = 'https://inshorts.com/en/read/technology'
    url4 = 'https://inshorts.com/en/read/entertainment'
    return [url1, url2, url3, url4]

def get_news():
    """ 
    Query, return dataframe of inshorts business, 
    sports, tech, entertainment articles 
    """
    # initialise empty dataframe
    df = pd.DataFrame() 
    # read each url in list
    for url in inshorts_urls(): 
        # add each dataframe of cards to df
        df = pd.concat([df, get_article(url)]) 
    # return all urls' cards
    return df 