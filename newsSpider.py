#!/usr/bin/env python3

from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer as ss
from fake_headers import Headers
from pprint import pprint
from pandas import DataFrame
from requests_futures.sessions import FuturesSession
from datetime import datetime

fake_headers = Headers(headers=True).generate()
url = {
'libertatea':'https://www.libertatea.ro/stiri-noi',
'digi24'	: 'https://www.digi24.ro/stiri/actualitate',
'mediafax'	: 'https://www.mediafax.ro/ultimele-stiri/',
'agerpres'	: 'https://www.agerpres.ro/'}


def start_session(url):
	
	with FuturesSession() as s:
		
		print(f'* Starting session for {url}')

		session 		= s.get(url, headers=fake_headers)
		soup 			= session.result()
		session_soup 	= bs(soup.text, 'lxml')

	return session_soup

# merge data to dict
def merge_data_to_dict(titles=None, links=None):
	
	varText 	= [text for text in titles]
	varLinks 	= [link for link in links]	
	dictionary	= dict(zip(varText,varLinks))
	
	print(f'* Merging into dictionaries...')
	
	return dictionary

# merge dictionaries to pass to DataFrame
def merge_dicts(*args: dict) -> dict:
	
	print('* Merging dictionaries to megaDict...')
	
	mega_dict = {}
	for arg in args:
		mega_dict.update(arg)
	
	return mega_dict

# output data to CSV
def create_csv(dictionary: dict, filename):
	
	print('* Exporting to CSV...')
	
	dataFrame = DataFrame(dictionary.items(), columns = ['Title', 'Link'])
	dataFrame.to_csv(f'{filename}.csv')


def get_text_libertatea(soup):
	
	print('* Parsing article titles for Libertatea...')
	
	for news_title in soup.find_all('h2', {'class' : 'article-title'}):
		
		yield news_title.a['title']

def get_links_libertatea(soup):
	
	print('* Parsing article links for Libertatea...')
	
	for news_links in soup.find_all('h2', {'class' : 'article-title'}):
		
		yield news_links.a['href']

def get_text_digi24(soup):
	
	print('* Parsing article titles for Digi24...')
	
	for news_title in soup.find_all('h4', {'class' : 'article-title'}):
		
		yield news_title.a['title']

def get_links_digi24(soup):
	
	print('* Parsing article links for Digi24...')
	
	for news_link in soup.find_all('h4', {'class' : 'article-title'}):
		
		yield f"{'https://www.digi24.ro'}{news_link.a['href']}"

def get_text_mediafax(soup):
	
	print('* Parsing article titles for Mediafax...')
	
	for news_title in soup.find_all('a', {'class':'item-title'}):
		
		yield news_title['title']

def get_links_mediafax(soup):
	
	print('* Parsing article links for Mediafax...')
	
	for news_links in soup.find_all('a', {'class':'item-title'}):
		
		yield news_links['href']

def get_text_agerpres(soup):
	
	print('* Parsing article titles for Agerpres...')
	
	for links in soup.find_all('div', {'class':'title_news'}):
		for link in links.find_all('h2'):
			
			yield link.string

def get_links_agerpres(soup):
	
	print('* Parsing article links for Agerpres...')
	
	for links in soup.find_all('div', {'class':'title_news'}):
		for link in links.find_all('h2'):
			
			yield f"{'https://www.agerpres.ro'}{link.a['href']}"