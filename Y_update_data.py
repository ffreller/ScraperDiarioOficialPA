from datetime import date
from C_PDFText import update_df
from pandas import read_csv
from B_downloader import download_bydate
from A_getlinks import update_links
from D_parsing import update_dfparsed

update_links('LinksDOE.csv')

df = read_csv('LinksDOE.csv', index_col='data')
today = date.today().strftime('%Y/%m/%d')
startdate = '2020/01/01'
enddate = today
dfdts = df.loc[startdate:enddate]
path1 = 'arquivos_DOE/'
download_bydate(dfdts, 'arquivos_DOE')

yr = 2020
path1 += f'{yr}/'
dfname = f'PDFs{yr}_index.csv'
df1 = update_df(path1, dfname)
if df1:
    df1.to_csv(f'PDFs{yr}_index.csv')

df2 = update_dfparsed(f'PDFs{yr}_index.csv', f'parsed{yr}.csv', path1)
if df2:
    df2.to_csv(f'parsed{yr}.csv')


