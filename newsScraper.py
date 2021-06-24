#!/usr/bin/env python3

import newsSpider

def scraping_time():

	responseLibertatea, responseDigi24, responseMediafax, responseAgerpres = newsSpider.start_session(
		newsSpider.url['libertatea'], newsSpider.url['digi24'], newsSpider.url['mediafax'], newsSpider.url['agerpres'])
	
	libertatea 	= newsSpider.libertatea_data(responseLibertatea)
	digi24 		= newsSpider.digi24_data(responseDigi24)
	mediafax 	= newsSpider.mediafax_data(responseMediafax)
	agerpres 	= newsSpider.agerpres_data(responseAgerpres)

	if not newsSpider.os.path.exists(newsSpider.os.path.join(newsSpider.os.getcwd(), 'CSV_OUTPUT')):
		newsSpider.Path('CSV_OUTPUT').mkdir(parents=False, exist_ok=True)
		newsSpider.os.chdir('CSV_OUTPUT')
		newsSpider.create_csv(libertatea, 	f"libertatea_{newsSpider.datetime.now().strftime('%H-%M')}")
		newsSpider.create_csv(digi24,		f"digi24_{newsSpider.datetime.now().strftime('%H-%M')}")
		newsSpider.create_csv(mediafax, 	f"mediafax_{newsSpider.datetime.now().strftime('%H-%M')}")
		newsSpider.create_csv(agerpres, 	f"agerpres_{newsSpider.datetime.now().strftime('%H-%M')}")
	
# magic the gathering #
if __name__ == '__main__':
	
	try:
		scraping_time()

	except KeyboardInterrupt:
		
		print('Exiting!')
		exit()