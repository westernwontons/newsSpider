#!/usr/bin/env python3

import os
import sys
from bs4 import BeautifulSoup
from fake_headers import Headers
from pprint import pprint
from pandas import DataFrame
from requests_futures.sessions import FuturesSession
from requests.exceptions import ConnectionError
from datetime import datetime
from pathlib import Path

fake_headers = Headers(headers=True).generate()
url = {
'libertatea': 'https://www.libertatea.ro/stiri-noi',
'digi24'	: 'https://www.digi24.ro/stiri/actualitate',
'mediafax'	: 'https://www.mediafax.ro/ultimele-stiri/',
'agerpres'	: 'https://www.agerpres.ro/'}


def start_session(url1, url2, url3, url4):

	with FuturesSession() as s:	
		print(f'[!] Starting sessions for [!]\n{url1}\n{url2}\n{url3}\n{url4}\n')
		print('-' * len(url3), '\n')

		session1		= s.get(url1, headers=fake_headers)
		session2		= s.get(url2, headers=fake_headers)
		session3		= s.get(url3, headers=fake_headers)
		session4		= s.get(url4, headers=fake_headers)

		soup1 			= session1.result()
		soup2			= session2.result()
		soup3			= session3.result()
		soup4			= session4.result()

		session_soup1 	= BeautifulSoup(soup1.text, 'lxml')
		session_soup2 	= BeautifulSoup(soup2.text, 'lxml')
		session_soup3 	= BeautifulSoup(soup3.text, 'lxml')
		session_soup4 	= BeautifulSoup(soup4.text, 'lxml')
			
	return session_soup1, session_soup2, session_soup3, session_soup4


def libertatea_data(soup):
	
	titles_list = list()
	links_list	= list()
	
	print('[+] Parsing data from Libertatea')
	
	titles = soup.find_all('h2', {'class' : 'article-title'})
	for news_title in titles:
		text_list = news_title.a['title']
		titles_list.append(text_list)

	links = soup.find_all('h2', {'class' : 'article-title'})
	for news_link in links:
		link_list = news_link.a['href']
		links_list.append(link_list)

	return zip(titles_list, links_list)

def digi24_data(soup):
	
	titles_list = list()
	links_list	= list()
	
	print('[+] Parsing data from Digi24')
	
	titles = soup.find_all('h4', {'class' : 'article-title'})
	for news_title in titles:
		text_list = news_title.a['title']
		titles_list.append(text_list)

	links = soup.find_all('h4', {'class' : 'article-title'})
	for news_link in links:
		link_list = news_link.a['href']
		links_list.append('https://www.digi24.ro/stiri/actualitate' + link_list)

	return zip(titles_list, links_list)

def mediafax_data(soup):
	
	titles_list = list()
	links_list	= list()
	
	print('[+] Parsing data from Mediafax')
	
	titles = soup.find_all('a', {'class':'item-title'})
	for news_title in titles:
		text_list = news_title['title']
		titles_list.append(text_list)

	links = soup.find_all('a', {'class':'item-title'})
	for news_link in links:
		the_links = news_link['href']
		if 'tags' in the_links:
			continue
		links_list.append(the_links)

	return zip(titles_list, links_list)

def agerpres_data(soup):

	titles_list = list()
	links_list	= list()

	print('[+] Parsing data from Agerpres', '\n')
	print('-' * len(url['digi24']))
	
	data = soup.find_all('div', {'class' : 'title_news'})
	
	for title in data:
		if len(title) != 1 or 'javascript:void(0)' not in title.a['href']:
			titles_list.append(title.h2.string)

	for links in data:
		if len(title) != 1 or 'javascript:void(0)' not in links.a['href']:
			links_list.append('https://www.agerpres.ro' + links.h2.a['href'])

	return zip(titles_list, links_list)

def create_csv(data, filename):
	
	print(f'[+] Exporting {filename} to CSV')

	dataFrame = DataFrame(data, columns=['Titles', 'Links'])
	dataFrame.to_csv(f'{filename}.csv', index=False)