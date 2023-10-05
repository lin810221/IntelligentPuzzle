import pandas as pd

# Defect reporting for QA review
def report_QA(*args):
    testPlan = args[0]
    fileName = args[1]
    fileCount = args[2]
    start_time = args[3]
    end_time = args[4]
    start_time_file_name = args[5]
    
    # 匯入 dataframe
    df_Result = testPlan[['用例編號', '測試項目', '測試標題', 'Result']]
    
    # 計算良率與不良率
    pass_count = df_Result['Result'].value_counts().get('Pass', 0)
    fail_count = df_Result['Result'].value_counts().get('Fail', 0)
    total_count = pass_count + fail_count
    
    pass_rate = (pass_count/total_count) * 100 if total_count > 0 else 0
    fail_rate = (fail_count/total_count) * 100 if total_count > 0 else 0
    
    title = fileName[fileCount].split('.')[0]
    head = '''
    <head>
        <meta charset="UTF-8">
        <title>QA Report</title>
        <style>
            table {
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid black;
                padding: 5px;
            }
            .pass {
                background-color: green;
                color: white;
            }
            .fail {
                background-color: red;
                color: white;
            }
        </style>
    </head>
    '''
    
    title_html = f'<h1>{title}</h1>'
    
    rate_html = f'<h3>良率：{pass_rate:.2f}%</h3>\
        <h3>不良率：{fail_rate:.2f}%</h3>'
    
    time_html = f'<p>開始時間：{start_time}</p>\
        <p>結束時間：{end_time}</p>'
    
    # 將 'Result' 欄位的值轉換為帶有對應 CSS class 的 HTML 標記
    df_Result['Result'] = df_Result['Result'].apply(lambda x: f'<td class="pass">{x}</td>' if x == 'Pass' else f'<td class="fail">{x}</td>')
    
    df_html = df_Result.to_html(index=False, escape=False)
    
    df_html = df_html.replace('<td><td class="fail">Fail</td></td>', '<td class="fail">Fail</td>').replace('<td><td class="pass">Pass</td></td>', '<td class="pass">Pass</td>')
    
    html_content = f'{head}{title_html}{rate_html}{time_html}{df_html}'
    
    with open(f'{title}_{start_time_file_name}.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
