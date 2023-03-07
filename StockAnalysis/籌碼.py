import requests
import numpy as np
import pandas as pd
from lxml import etree

########################################################################################
#                                    法人買賣
########################################################################################
url = 'https://tw.stock.yahoo.com/quote/5425.TWO/institutional-trading'
res = requests.get(url)
html = res.content.decode()
element = etree.HTML(html)

# 更新時間
update_time = element.xpath('//*[@id="qsp-trading-variant"]/div[1]/time/span[2]/text()')

# 法人買賣總覽
title = element.xpath('//*[@id="qsp-trading-summary"]/div/div/div/div/div/text()')
index = element.xpath('//*[@id="qsp-trading-summary"]/div[3]/div/div/div[2]/ul/li/div/div/div/span/text()')
trade = element.xpath('//*[@id="qsp-trading-summary"]/div/div/div/div/ul/li/div/div/span/text()')
trade = np.array(trade).reshape(len(index), len(title))
institutional_investors = pd.DataFrame(trade, index=index, columns=title) # 三大法人
print(institutional_investors)


# 法人逐日買賣超
title = element.xpath('//*[@id="qsp-trading-by-day"]/div[3]/div/div/div/div[1]/div/text()')
index = element.xpath('//*[@id="qsp-trading-by-day"]/div[3]/div/div/div/div[2]/ul/li/div/div/div/text()')
trade = element.xpath('//*[@id="qsp-trading-by-day"]/div[3]/div/div/div/div[2]/ul/li/div/div/span/text()')
trade = np.array(trade).reshape(len(index), len(title))

institutional_investors_stock = pd.DataFrame(trade, index=index, columns=title)
print(institutional_investors_stock)

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
url = 'https://tw.stock.yahoo.com/quote/5425.TWO/margin'
res = requests.get(url)
html = res.content.decode()
element = etree.HTML(html)

columns=['增減', '餘額', '使用率 %']

# 日期
date_trade = element.xpath('//*[@id="qsp-margin-balance-by-date"]/div[3]/div/div/div[2]/ul/li/div/div[1]/div[1]/text()')

# 融資
margin_trade = element.xpath('//*[@id="qsp-margin-balance-by-date"]/div[3]/div/div/div[2]/ul/li/div/div[2]/ul/li/span/text()')
margin_trade = np.array(margin_trade).reshape(len(date_trade), int(len(margin_trade)/len(date_trade)))
margin_trade = pd.DataFrame(margin_trade, index=date_trade, columns=columns)

# 融券
short_selling = element.xpath('//*[@id="qsp-margin-balance-by-date"]/div[3]/div/div/div[2]/ul/li/div/div[3]/ul/li/span/text()')
short_selling = np.array(short_selling).reshape(len(date_trade), int(len(short_selling)/len(date_trade)))
short_selling = pd.DataFrame(short_selling, index=date_trade, columns=columns)

# 融資融券比
title = element.xpath('//*[@id="qsp-margin-balance-by-date"]/div[3]/div/div/div[1]/div/span/text()')
bonds = element.xpath('//*[@id="qsp-margin-balance-by-date"]/div[3]/div/div/div[2]/ul/li/div/div/span/text()')
bonds = np.array(bonds).reshape(len(date_trade), int(len(bonds)/len(date_trade)))
bonds = pd.DataFrame(bonds, index=date_trade, columns=title)


Margin_financing = pd.concat([margin_trade, short_selling, bonds], axis=1, keys=['融資', '融券', '資券行情'])
print(Margin_financing)

########################################################################################
#                                    大戶籌碼
########################################################################################
url = 'https://tw.stock.yahoo.com/quote/5425.TWO/major-holders'
res = requests.get(url)
html = res.content.decode()
element = etree.HTML(html)

# 更新日期
update_time = element.xpath('//*[@id="main-3-QuoteChipMajorHolders-Proxy"]/div/section[2]/div[1]/time/span[2]/text()')

# 大戶籌碼
title = element.xpath('//*[@id="main-3-QuoteChipMajorHolders-Proxy"]/div/section[2]/div/div/div/div/div/text()')
date = element.xpath('//*[@id="main-3-QuoteChipMajorHolders-Proxy"]/div/section[2]/div[2]/div/div/div[2]/ul/li/div/div[1]/div/span/text()')
major_holders = element.xpath('//*[@id="main-3-QuoteChipMajorHolders-Proxy"]/div/section[2]/div[2]/div/div/div[2]/ul/li/div/div/span/text()')
major_holders = np.array(major_holders).reshape(len(date), int(len(major_holders) / len(date)))
major_holders = pd.DataFrame(major_holders, index=date, columns=title)
print(major_holders)
