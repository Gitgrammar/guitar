import datetime
import urllib
import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

URL_MERCARI ="https://www.mercari.com/jp/search/?sort_order=price_asc&keyword={}&status_on_sale=1"
URL_RAKUMA="https://fril.jp/search/{}?order=asc&sort=sell_price&transaction=selling"

SELECTOR_MERCARI='.items-box-price'
SELECTOR_RAKUMA='.items-box_price'

CAT_CHAR=''
NOT_CHAR='-'
DATA_FILE='data.csv'

keywords_all=[
	{
	'and':['Ibanez', 'TS-9'],
	'not':['TS9DX', '808','TS5']
	},
	{
	'and':['Ibanez', 'RG350'],
	'not':['ジャンク']
	},
	{
	'and':['BOSS', 'GT-1','エフェクター'],
	'not':['GT-10','GT-100','GT-1000','GT-1B','ACアダプタ','教科書']
	},
]

def get_min_price(browser,base_url,query_params,selector):
		dic=str.marketrans({
				'¥':'',
				'￥':'',
				',':'',
			})
		url=base_url.format(urllib.parse.quote(query_params))
		try:
				browser.get(url)
				elm_min=browser.find_element_by_css_selector(selector)
		except NoSuchElementException as e:
				print(f'指定した要素が見つかりませんでした:{e.args}')
	except TimeoutException as e:
				print(f'読み込みがタイムアウトしました:{e.args}')
		return(elm_min.text.translate(dic))

browser =webdriver.Chrome('chromedriver.exe')
browser.set_page_load_timeout(30)

record=[]

record.append(datetime.date.today().strftime('%y/%m/%d'))

for keywords in keywords_all:

	query_params_and=CAT_CHAR.join(keywords['and'])
	query_params_not=CAT_CHAR.join([NOT_CHAR+kw for kw  in keywords['not']])

	query_params_mercari=query_params_and +query_params_not
	min_price=get_min_price(browser,URL_MERCARI,query_params_mercari,SELECTOR_MERCARI)
	record.append(min_price)
	
	
	query_params_rakuma =query_params_and 
	min_price=get_min_price(browser,URL_RAKUMA,query_params_rakuma,SELECTOR_RAKUMA)
	record.append(min_price)

browser.quit()

try:
		with open(DATA_FILE,'a',newline='')as f:
				writer=csv.writer(f,delimiter=',')
				writer.writerow(record)
	
except OSError as e:
		print(f'ファイル処理でエラー発生:{e.args}')
