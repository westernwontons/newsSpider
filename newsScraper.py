#!/usr/bin/env python3

import newsSpider

def main():
	responseLibertatea 	= newsSpider.start_session(newsSpider.url['libertatea'])
	responseDigi24	 	= newsSpider.start_session(newsSpider.url['digi24'])
	responseMediafax 	= newsSpider.start_session(newsSpider.url['mediafax'])
	responseAgerpres 	= newsSpider.start_session(newsSpider.url['agerpres'])

	textLibertatea,	linkLibertatea 	= newsSpider.get_text_libertatea(responseLibertatea), newsSpider.get_links_libertatea(responseLibertatea)
	textDigi24, 	linkDigi24 		= newsSpider.get_text_digi24(responseDigi24), newsSpider.get_links_digi24(responseDigi24)
	textMediafax, 	linkMediafax 	= newsSpider.get_text_mediafax(responseMediafax), newsSpider.get_links_mediafax(responseMediafax)
	textAgerpres, 	linkAgerpres	= newsSpider.get_text_agerpres(responseAgerpres), newsSpider.get_links_agerpres(responseAgerpres)

	dataLibertatea 	= newsSpider.merge_data_to_dict(titles=textLibertatea, links=linkLibertatea)
	dataDigi24		= newsSpider.merge_data_to_dict(titles=textDigi24, 	links=linkDigi24)
	dataMediafax 	= newsSpider.merge_data_to_dict(titles=textMediafax,	links=linkMediafax)
	dataAgerpres 	= newsSpider.merge_data_to_dict(titles=textAgerpres, 	links=linkAgerpres)

	newsSpider.create_csv(dataLibertatea, 	f"libertatea {newsSpider.datetime.now().strftime('%H-%M')}")
	newsSpider.create_csv(dataDigi24, 		f"digi24 {newsSpider.datetime.now().strftime('%H-%M')}")
	newsSpider.create_csv(dataMediafax, 	f"mediafax {newsSpider.datetime.now().strftime('%H-%M')}")
	newsSpider.create_csv(dataAgerpres, 	f"agerpres {newsSpider.datetime.now().strftime('%H-%M')}")

# magic the gathering
if __name__ == '__main__':
	main()

