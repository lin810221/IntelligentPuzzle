import requests
import numpy as np
import pandas as pd
from lxml import etree

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
#                                    法人買賣
########################################################################################
# 法人買賣總覽
info = {'url':'https://tw.stock.yahoo.com/quote/5425.TWO/institutional-trading',
        'update_time': '//*[@id="qsp-trading-variant"]/div[1]/time/span[2]/text()',
        'title':'//*[@id="qsp-trading-summary"]/div/div/div/div/div/text()',
        'index':'//*[@id="qsp-trading-summary"]/div[3]/div/div/div[2]/ul/li/div/div/div/span/text()',
        'data':'//*[@id="qsp-trading-summary"]/div/div/div/div/ul/li/div/div/span/text()'}

institutional_investors = crawler(info); print(institutional_investors)

# 法人逐日買賣超
info = {'url':'https://tw.stock.yahoo.com/quote/5425.TWO/institutional-trading',
        'update_time':'//*[@id="qsp-trading-variant"]/div[1]/time/span[2]/text()',
        'title':'//*[@id="qsp-trading-by-day"]/div[3]/div/div/div/div[1]/div/text()',
        'index':'//*[@id="qsp-trading-by-day"]/div[3]/div/div/div/div[2]/ul/li/div/div/div/text()',
        'data':'//*[@id="qsp-trading-by-day"]/div[3]/div/div/div/div[2]/ul/li/div/div/span/text()'}

institutional_investors_stock = crawler(info); print(institutional_investors_stock)

########################################################################################
#                                    主力進出
########################################################################################

url = 'https://tw.stock.yahoo.com/quote/5425.TWO/broker-trading'
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
info = {'url':'https://tw.stock.yahoo.com/quote/5425.TWO/margin',
        'update_time':'//*[@id="qsp-margin-summary"]/div[1]/span/time/span[2]/text()',
        'title':'//*[@id="qsp-margin-balance-by-date"]/div[3]/div/div/div[1]/div[3]/div/ul/li/text()',
        'index':'//*[@id="qsp-margin-balance-by-date"]/div[3]/div/div/div[2]/ul/li/div/div[1]/div[1]/text()',
        'data':'//*[@id="qsp-margin-balance-by-date"]/div[3]/div/div/div[2]/ul/li/div/div[2]/ul/li/span/text()'}

margin_trade = crawler(info)

# 融券
info = {'url':'https://tw.stock.yahoo.com/quote/5425.TWO/margin',
        'update_time':'//*[@id="qsp-margin-summary"]/div[1]/span/time/span[2]/text()',
        'title':'//*[@id="qsp-margin-balance-by-date"]/div[3]/div/div/div[1]/div[3]/div/ul/li/text()',
        'index':'//*[@id="qsp-margin-balance-by-date"]/div[3]/div/div/div[2]/ul/li/div/div[1]/div[1]/text()',
        'data':'//*[@id="qsp-margin-balance-by-date"]/div[3]/div/div/div[2]/ul/li/div/div[3]/ul/li/span/text()'}

short_selling = crawler(info)

# 融資融券比
info = {'url':'https://tw.stock.yahoo.com/quote/5425.TWO/margin',
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
info = {'url':'https://tw.stock.yahoo.com/quote/5425.TWO/major-holders',
        'update_time':'//*[@id="main-3-QuoteChipMajorHolders-Proxy"]/div/section[2]/div[1]/time/span[2]/text()',
        'title':'//*[@id="main-3-QuoteChipMajorHolders-Proxy"]/div/section[2]/div/div/div/div/div/text()',
        'index':'//*[@id="main-3-QuoteChipMajorHolders-Proxy"]/div/section[2]/div[2]/div/div/div[2]/ul/li/div/div[1]/div/span/text()',
        'data':'//*[@id="main-3-QuoteChipMajorHolders-Proxy"]/div/section[2]/div[2]/div/div/div[2]/ul/li/div/div/span/text()'}

major_holders = crawler(info)
print(major_holders)


########################################################################################
#                                    營收表
########################################################################################
info = {'url':'https://tw.stock.yahoo.com/quote/5425.TWO/revenue',
        'update_time':'//*[@id="main-0-QuoteHeader-Proxy"]/div/div/div/span/text()',
        'title':'//*[@id="qsp-revenue-table"]/div/div/div/div[1]/div/div/ul/li/text()',
        'index':'//*[@id="qsp-revenue-table"]/div/div/div/div[2]/ul/li/div/div[1]/div[1]/text()',
        'data':'//*[@id="qsp-revenue-table"]/div/div/div/div[2]/ul/li/div/div/ul/li/span/text()'}
revenue = crawler(info)
print(revenue)

########################################################################################
#                                    每股盈餘
########################################################################################

info = {'url':'https://tw.stock.yahoo.com/quote/5425.TWO/eps',
        'update_time':'//*[@id="main-0-QuoteHeader-Proxy"]/div/div[2]/div[1]/span/text()',
        'title':'//*[@id="qsp-eps-table"]/div/div/div/div[1]/div/text()',
        'index':'//*[@id="qsp-eps-table"]/div/div/div/div/ul/li/div/div/div/text()',
        'data':'//*[@id="qsp-eps-table"]/div/div/div/div[2]/ul/li/div/div/span/text()'}

eps = crawler(info)
print(eps)

########################################################################################
#                                    損益表
########################################################################################
info = {'url':'https://tw.stock.yahoo.com/quote/5425.TWO/income-statement',
        'update_time':'//*[@id="main-0-QuoteHeader-Proxy"]/div/div[2]/div[1]/span/text()',
        'title':'//*[@id="qsp-income-statement-table"]/div/div/div/div[1]/div/text()',
        'index':'//*[@id="qsp-income-statement-table"]/div/div/div/div[2]/ul/li/div/div[1]/div[1]/span/text()',
        'data':'//*[@id="qsp-income-statement-table"]/div/div/div/div[2]/ul/li/div/div/span/text()'}

income_statement = crawler(info)
print(income_statement)


########################################################################################
#                                    資產負債表
########################################################################################
info = {'url':'https://tw.stock.yahoo.com/quote/5425.TWO/balance-sheet',
        'update_time':'//*[@id="main-0-QuoteHeader-Proxy"]/div/div[2]/div[1]/span/text()',
        'title':'//*[@id="qsp-balance-sheet-table"]/div/div/div/div[1]/div/text()',
        'index':'//*[@id="qsp-balance-sheet-table"]/div/div/div/div[2]/ul/li/div/div[1]/div[1]/span/text()',
        'data':'//*[@id="qsp-balance-sheet-table"]/div/div/div/div[2]/ul/li/div/div/span/text()'}

balance_sheet = crawler(info)
print(balance_sheet)

########################################################################################
#                                    現金流量表
########################################################################################
info = {'url':'https://tw.stock.yahoo.com/quote/5425.TWO/cash-flow-statement',
        'update_time':'//*[@id="main-0-QuoteHeader-Proxy"]/div/div[2]/div[1]/span/text()',
        'title':'//*[@id="qsp-cash-flow-statement-table"]/div/div/div/div[1]/div/text()',
        'index':'//*[@id="qsp-cash-flow-statement-table"]/div/div/div/div[2]/ul/li/div/div[1]/div[1]/span/text()',
        'data':'//*[@id="qsp-cash-flow-statement-table"]/div/div/div/div[2]/ul/li/div/div/span/text()'}

cash_flow_state = crawler(info)
print(cash_flow_state)
