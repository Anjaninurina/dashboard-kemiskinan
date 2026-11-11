import pandas as pd
for nama in ['kemiskinan', 'ipm', 'tpt', 'rls']:
    xls = pd.ExcelFile('data/raw/' + nama + '.xlsx')
    print('=====', nama, 'sheet:', xls.sheet_names)
    df = pd.read_excel(xls, header=None)
    print(df.shape)
    print(df.head(8).to_string())
    print(df.tail(3).to_string())
    
                       