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
    agent = 'codeup ds germain' # setting the agent so Codeup site doesn't block our web-scraper
    response = requests.get(url, headers={'User-Agent': agent}) # query
    soup = BeautifulSoup(response.text) # soup
    articles = soup.select('.grid.gap-y-12 > div') # raw list of articles
    article_list = [] # initialise list of dicts for dataframe
    for article in articles: # parse each article
        title = article.h2.text # grab title
        date, author, contents = article.select('.py-3')[0]\
            .find_all('p') # grab date, author, contents of article
        article_list.append({'title':title, 'date':date.text, 
            'author':author.text, 'contents':contents.text}) # add dict of info to list
    
    return pd.DataFrame(article_list) # return dataframe

def parse_gulde_people():
    """ 
    Returns dataframe of scraped web-scraping-demo.zgulde.net/people 
    """
    url = 'https://web-scraping-demo.zgulde.net/people' # set the url
    agent = 'codeup ds germain'
    response = requests.get(url, headers={'User-Agent': agent}) # query
    soup = BeautifulSoup(response.text) # soup
    people = soup.find_all('div', {'class':'person'}) # raw list of people
    info_list = [] # initialise list of dicts for dataframe
    for person in people: # parse each person
        name = person.h2.text # grab name
        quote, email, phone, address = person.find_all('p') # grab more info
        # fix info
        quote, email, phone, address = quote.text.strip(), email.text, phone.text, address.text.strip()
        regexp = r'\s{2,}' # set regex for address fix
        address = re.sub(regexp, ' ', address) # fix address
        person_dict = {'name':name, 'quote':quote, 'email':email, 
                       'phone':phone, 'address':address} # create dict
        info_list.append(person_dict) # add dict to list

    return pd.DataFrame(info_list) # return dataframe

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
    agent = 'codeup ds germain' # set the agent
    response = requests.get(url, headers={'User-Agent': agent}) # query
    soup = BeautifulSoup(response.text, features="lxml") # soup, added features argument to prevent warning
    title = soup.select('.entry-title')[0].text # get title
    date = soup.select('.published')[0].text # get date
    category = soup.find_all('a', {'rel':'category tag'})[0].text # get category
    # grab all unformatted paragraphs
    paragraphs = soup.find_all('div', {'class':'et_pb_module et_pb_post_content et_pb_post_content_0_tb_body'})[0]\
    .find_all('p')
    paragraph_list = [] # create list for formatted paragraphs
    for paragraph in paragraphs: # iterate paragraphs
        paragraph_list.append(paragraph.text) # add to list
    content = " ".join(paragraph_list).replace('\xa0', ' ') # destroy href markers
    # create dict
    blog_info_dict = {'title':title, 'date':date, 'category':category, 'content':content}
    # return dict
    return blog_info_dict

def get_blogs():
    """ 
    Queries, returns a dataframe of each codeup blog article's stuff 
    """
    list_of_blog_dicts = [] # initialise the dictionary
    for url in codeup_blog_urls():
        list_of_blog_dicts.append(acquire_codeup_blog(url)) # add each blog to the list of blogs dictionary
    return pd.DataFrame(list_of_blog_dicts)

def get_article(url):
    """ 
    Return dataframe of articles in inshorts category URL 
    """
    agent = 'codeup ds germain' # set the agent
    response = requests.get(url, headers={'User-Agent': agent}) # query
    soup = BeautifulSoup(response.text, features="lxml") # soup, added features argument to prevent warning
    category = soup.find_all('li', {'class':'active-category selected'})[0].text # get category
    cards = soup.select('.news-card') # get raw cards
    card_dict_list = [] # create list of dicts for dataframe
    for card in cards: # iterate each card
        headline = card.find_all('span', {'itemprop':'headline'})[0].text # headline
        publish_time = card.find_all('span', {'class':'time'})[0].text # publish time
        content = card.find_all('div', {'itemprop':'articleBody'})[0].text.strip() # content
        card_dict = {'headline':headline, 'publish_time':publish_time,
                       'category':category, 'content':content} # create dict
        card_dict_list.append(card_dict) # push dict to list
    return pd.DataFrame(card_dict_list) # return dataframe

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
    df = pd.DataFrame() # initialise empty dataframe
    for url in inshorts_urls(): # read each url in list
        df = pd.concat([df, get_article(url)]) # add each dataframe of cards to df
    return df # return all urls' cards