import requests
import os
import numpy as np
import pandas as pd
from lxml import etree

########################################################################################
#                                    讀取/爬取 證券一覽表
########################################################################################
def crawler_StockList(url, market):    
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36"}
    response = requests.get(url, headers=headers, verify=False)
    html = response.text
    element = etree.HTML(html)
    
    code_name = element.xpath('//tr/td[1]/text()')
    df = pd.DataFrame()
    
    for i in code_name[1:]:
        df = df.append({'code':i.split('\u3000')[0], 'company':i.split('\u3000')[1]}, ignore_index=True)
    df['market'] = market
    return df


def StockList():
    url = ['https://isin.twse.com.tw/isin/C_public.jsp?strMode=2',
           'https://isin.twse.com.tw/isin/C_public.jsp?strMode=4']
    market = ['上市', '上櫃']
    print('正在爬取 "本國上市證券國際證券辨識號碼一覽表"')
    OTC = crawler_StockList(url[0], market[0])
    print('正在爬取 "本國上櫃證券國際證券辨識號碼一覽表"')
    TSE = crawler_StockList(url[1], market[1])
    df = pd.concat([OTC, TSE], axis=0)
    n = len(OTC) + len(TSE)
    df.index = range(n)
    df.to_csv('證券國際證券辨識號碼一覽表.csv', encoding='utf-8-sig', index=False)

try:
    df_StockList = pd.read_csv('證券國際證券辨識號碼一覽表.csv')
    df_StockList
except:
    print('當下找不到檔案，立即建立資料表')
    StockList()


########################################################################################
#                                    Crawler Function
########################################################################################
'''
更新日期 - update_time
行名稱 - title
列名稱 - index
資料 - data

info = {'url':'',
        'update_time':'',
        'title':'',
        'index':'',
        'data':''}
'''
def crawler(res):
    url = info.get('url')
    res = requests.get(url)
    html = res.content.decode()
    element = etree.HTML(html)
    
    try:
        # 更新時間
        update_time = element.xpath(info.get('update_time'))
        print(update_time)
        
        # 法人買賣總覽
        title = element.xpath(info.get('title'))
        index = element.xpath(info.get('index'))
        data = element.xpath(info.get('data'))
        data = np.array(data).reshape(len(index), len(title))
        institutional_investors = pd.DataFrame(data, index=index, columns=title) # 三大法人
        return institutional_investors
    
    except:
        print('疑似有缺失值，等待官網更新！')


########################################################################################
#                                    【Start】
########################################################################################
StockNumber = input('請輸入股號：')

# 在證券一覽表搜尋
try:
    Stock = df_StockList[df_StockList['code'] == StockNumber]
    stock = StockNumber + '.' + ('TW' if list(Stock['market'])[0] == '上市' else 'TWO')
    company_name = list(Stock['company'])[0]
except:
    print('找不到該公司')


########################################################################################
#                                    法人買賣
########################################################################################
# 法人買賣總覽
info = {'url':'https://tw.stock.yahoo.com/quote/' + stock +'/institutional-trading',
        'update_time': '//*[@id="qsp-trading-variant"]/div[1]/time/span[2]/text()',
        'title':'//*[@id="qsp-trading-summary"]/div/div/div/div/div/text()',
        'index':'//*[@id="qsp-trading-summary"]/div[3]/div/div/div[2]/ul/li/div/div/div/span/text()',
        'data':'//*[@id="qsp-trading-summary"]/div/div/div/div/ul/li/div/div/span/text()'}

institutional_investors = crawler(info); print(institutional_investors)

# 法人逐日買賣超
info = {'url':'https://tw.stock.yahoo.com/quote/' + stock + '/institutional-trading',
        'update_time':'//*[@id="qsp-trading-variant"]/div[1]/time/span[2]/text()',
        'title':'//*[@id="qsp-trading-by-day"]/div[3]/div/div/div/div[1]/div/text()',
        'index':'//*[@id="qsp-trading-by-day"]/div[3]/div/div/div/div[2]/ul/li/div/div/div/text()',
        'data':'//*[@id="qsp-trading-by-day"]/div[3]/div/div/div/div[2]/ul/li/div/div/span/text()'}

institutional_investors_stock = crawler(info); print(institutional_investors_stock)

########################################################################################
#                                    主力進出
########################################################################################

url = 'https://tw.stock.yahoo.com/quote/' + stock + '/broker-trading'
res = requests.get(url)
html = res.content.decode()
element = etree.HTML(html)
#更新時間
update_time = element.xpath('//*[@id="main-3-QuoteChipMajor-Proxy"]/div/div[1]/span/time/span[2]/text()')

# 主力進出
title = element.xpath('//*[@id="main-3-QuoteChipMajor-Proxy"]/div/div[2]/div/div/div[1]/text()')
trade = element.xpath('//*[@id="main-3-QuoteChipMajor-Proxy"]/div/div[2]/div/div/div[2]/text()')
trade = np.array(trade).reshape(1, len(title))

broker_trade = pd.DataFrame(trade, columns=title)
print(broker_trade)

########################################################################################
#                                    資券變化
########################################################################################
# 融資
info = {'url':'https://tw.stock.yahoo.com/quote/' + stock + '/margin',
        'update_time':'//*[@id="qsp-margin-summary"]/div[1]/span/time/span[2]/text()',
        'title':'//*[@id="qsp-margin-balance-by-date"]/div[3]/div/div/div[1]/div[3]/div/ul/li/text()',
        'index':'//*[@id="qsp-margin-balance-by-date"]/div[3]/div/div/div[2]/ul/li/div/div[1]/div[1]/text()',
        'data':'//*[@id="qsp-margin-balance-by-date"]/div[3]/div/div/div[2]/ul/li/div/div[2]/ul/li/span/text()'}

margin_trade = crawler(info)

# 融券
info = {'url':'https://tw.stock.yahoo.com/quote/' + stock + '/margin',
        'update_time':'//*[@id="qsp-margin-summary"]/div[1]/span/time/span[2]/text()',
        'title':'//*[@id="qsp-margin-balance-by-date"]/div[3]/div/div/div[1]/div[3]/div/ul/li/text()',
        'index':'//*[@id="qsp-margin-balance-by-date"]/div[3]/div/div/div[2]/ul/li/div/div[1]/div[1]/text()',
        'data':'//*[@id="qsp-margin-balance-by-date"]/div[3]/div/div/div[2]/ul/li/div/div[3]/ul/li/span/text()'}

short_selling = crawler(info)

# 融資融券比
info = {'url':'https://tw.stock.yahoo.com/quote/' + stock + '/margin',
        'update_time':'//*[@id="qsp-margin-summary"]/div[1]/span/time/span[2]/text()',
        'title':'//*[@id="qsp-margin-balance-by-date"]/div[3]/div/div/div[1]/div/span/text()',
        'index':'//*[@id="qsp-margin-balance-by-date"]/div[3]/div/div/div[2]/ul/li/div/div[1]/div[1]/text()',
        'data':'//*[@id="qsp-margin-balance-by-date"]/div[3]/div/div/div[2]/ul/li/div/div/span/text()'}


bonds = crawler(info)


Margin_financing = pd.concat([margin_trade, short_selling, bonds], axis=1, keys=['融資', '融券', '資券行情'])
print(Margin_financing)

########################################################################################
#                                    大戶籌碼
########################################################################################
info = {'url':'https://tw.stock.yahoo.com/quote/' + stock + '/major-holders',
        'update_time':'//*[@id="main-3-QuoteChipMajorHolders-Proxy"]/div/section[2]/div[1]/time/span[2]/text()',
        'title':'//*[@id="main-3-QuoteChipMajorHolders-Proxy"]/div/section[2]/div/div/div/div/div/text()',
        'index':'//*[@id="main-3-QuoteChipMajorHolders-Proxy"]/div/section[2]/div[2]/div/div/div[2]/ul/li/div/div[1]/div/span/text()',
        'data':'//*[@id="main-3-QuoteChipMajorHolders-Proxy"]/div/section[2]/div[2]/div/div/div[2]/ul/li/div/div/span/text()'}

major_holders = crawler(info)
print(major_holders)


########################################################################################
#                                    營收表
########################################################################################
info = {'url':'https://tw.stock.yahoo.com/quote/' + stock + '/revenue',
        'update_time':'//*[@id="main-0-QuoteHeader-Proxy"]/div/div/div/span/text()',
        'title':'//*[@id="qsp-revenue-table"]/div/div/div/div[1]/div/div/ul/li/text()',
        'index':'//*[@id="qsp-revenue-table"]/div/div/div/div[2]/ul/li/div/div[1]/div[1]/text()',
        'data':'//*[@id="qsp-revenue-table"]/div/div/div/div[2]/ul/li/div/div/ul/li/span/text()'}
revenue = crawler(info)
print(revenue)

########################################################################################
#                                    每股盈餘
########################################################################################

info = {'url':'https://tw.stock.yahoo.com/quote/' + stock + '/eps',
        'update_time':'//*[@id="main-0-QuoteHeader-Proxy"]/div/div[2]/div[1]/span/text()',
        'title':'//*[@id="qsp-eps-table"]/div/div/div/div[1]/div/text()',
        'index':'//*[@id="qsp-eps-table"]/div/div/div/div/ul/li/div/div/div/text()',
        'data':'//*[@id="qsp-eps-table"]/div/div/div/div[2]/ul/li/div/div/span/text()'}

eps = crawler(info)
print(eps)

########################################################################################
#                                    損益表
########################################################################################
info = {'url':'https://tw.stock.yahoo.com/quote/' + stock + '/income-statement',
        'update_time':'//*[@id="main-0-QuoteHeader-Proxy"]/div/div[2]/div[1]/span/text()',
        'title':'//*[@id="qsp-income-statement-table"]/div/div/div/div[1]/div/text()',
        'index':'//*[@id="qsp-income-statement-table"]/div/div/div/div[2]/ul/li/div/div[1]/div[1]/span/text()',
        'data':'//*[@id="qsp-income-statement-table"]/div/div/div/div[2]/ul/li/div/div/span/text()'}

income_statement = crawler(info)
print(income_statement)


########################################################################################
#                                    資產負債表
########################################################################################
info = {'url':'https://tw.stock.yahoo.com/quote/' + stock + '/balance-sheet',
        'update_time':'//*[@id="main-0-QuoteHeader-Proxy"]/div/div[2]/div[1]/span/text()',
        'title':'//*[@id="qsp-balance-sheet-table"]/div/div/div/div[1]/div/text()',
        'index':'//*[@id="qsp-balance-sheet-table"]/div/div/div/div[2]/ul/li/div/div[1]/div[1]/span/text()',
        'data':'//*[@id="qsp-balance-sheet-table"]/div/div/div/div[2]/ul/li/div/div/span/text()'}

balance_sheet = crawler(info)
print(balance_sheet)

########################################################################################
#                                    現金流量表
########################################################################################
info = {'url':'https://tw.stock.yahoo.com/quote/' + stock + '/cash-flow-statement',
        'update_time':'//*[@id="main-0-QuoteHeader-Proxy"]/div/div[2]/div[1]/span/text()',
        'title':'//*[@id="qsp-cash-flow-statement-table"]/div/div/div/div[1]/div/text()',
        'index':'//*[@id="qsp-cash-flow-statement-table"]/div/div/div/div[2]/ul/li/div/div[1]/div[1]/span/text()',
        'data':'//*[@id="qsp-cash-flow-statement-table"]/div/div/div/div[2]/ul/li/div/div/span/text()'}

cash_flow_state = crawler(info)
print(cash_flow_state)

########################################################################################
#                                    儲存至 Excel
########################################################################################
path = os.path.join(os.getcwd(), company_name + '.xlsx')
writer = pd.ExcelWriter(path, engine='openpyxl')

institutional_investors.to_excel(writer, sheet_name='法人買賣總覽')
institutional_investors_stock.to_excel(writer, sheet_name='法人逐日買賣超')
broker_trade.to_excel(writer, sheet_name='主力進出')
Margin_financing.to_excel(writer, sheet_name='資券變化')
major_holders.to_excel(writer, sheet_name='大戶籌碼')
revenue.to_excel(writer, sheet_name='營收表')
eps.to_excel(writer, sheet_name='每股盈餘')
income_statement.to_excel(writer, sheet_name='損益表')
balance_sheet.to_excel(writer, sheet_name='資產負債表')
cash_flow_state.to_excel(writer, sheet_name='現金流量表')

writer.save() # 存檔生成excel檔案
