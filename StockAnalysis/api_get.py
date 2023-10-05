import requests
import pandas as pd

def api_get(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return []

def fetch_data(endpoint, column_mapping, category):
    data = api_get(endpoint)
    return [{column: entry.get(mapping) for column, mapping in column_mapping.items()} for entry in data]

def main():
    endpoints = [
        ('https://openapi.twse.com.tw/v1/opendata/t187ap03_L', {'公司代號': '公司代號', '公司名稱': '公司名稱', '公司簡稱': '公司簡稱', '產業別': '產業別'}, '上市'),
        ('https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap03_O', {'公司代號': 'SecuritiesCompanyCode', '公司名稱': 'CompanyName', '公司簡稱': '公司簡稱', '產業別': 'SecuritiesIndustryCode'}, '上櫃'),
        ('https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap03_R', {'公司代號': 'SecuritiesCompanyCode', '公司名稱': 'CompanyName', '公司簡稱': '公司簡稱', '產業別': 'SecuritiesIndustryCode'}, '興櫃'),
    ]

    df = pd.concat([pd.DataFrame(fetch_data(endpoint, column_mapping, category), columns=['公司代號', '公司名稱', '公司簡稱', '產業別']).assign(分類=category) for endpoint, column_mapping, category in endpoints], ignore_index=True)
    df.set_index('公司代號', inplace=True)
    return df

if __name__ == "__main__":
    df = main()
    df.to_csv('Output.csv', sep = ',', index = True, header = True, encoding='utf-8-sig')
