# import pdfplumber
# from pandas import read_csv, concat, DataFrame
# from Z1_regex import parse_text, inconsistencias, corrigir_texto
# from ast import literal_eval
# from tqdm import tqdm
# from datetime import datetime
#
#
# def get_location(startpage, path, filename):
#     data = datetime.strptime(filename[4:14], '%Y-%m-%d')
#     data2 = datetime.strptime('2019-03-01', '%Y-%m-%d')
#     characs = []
#     pal = ''
#     check1 = False
#     check2 = False
#     with pdfplumber.open(path + filename) as pdf:
#         npage = startpage - 1
#         page = pdf.pages[npage]
#
#         for c, cha in enumerate(page.chars):
#             rsize = round(float(cha['width']) / float(cha['adv']))
#             if check1:
#                 characs.append(cha)
#                 if rsize == 12:
#                     if filename == 'DOE_2018-05-29.pdf':
#                         break
#                     check2 = True
#                     break
#             if not check1 and rsize == 12:
#                 pal += cha['text']
#                 if 'TERRAS DO PARÁ' in pal:
#                     check1 = True
#
#         while not check2:
#             npage += 1
#             page = pdf.pages[npage]
#             for c, linha in enumerate(page.lines):
#                 if c == 0:
#                     dist = float(linha['bottom'])
#                     break
#             for c, cha in enumerate(page.chars):
#                 rsize = round(float(cha['width']) / float(cha['adv']))
#                 if float(cha['bottom']) > dist:
#                     characs.append(cha)
#                     if rsize == 12:
#                         check2 = True
#                         break
#
#     res = []
#     lim1, lim2, lim3, lim4 = 285, 285, 533, 534
#
#
#     if data < data2:
#         for ch in characs:
#             col_loc = 0
#             if float(ch['x0']) < lim1:
#                 col_loc = 1
#             if lim2 < float(ch['x0']) < lim3:
#                 col_loc = 2
#             if float(ch['x0']) > lim4:
#                 col_loc = 3
#             if col_loc == 0:
#                 print('Ainda com problema', filename, ch['page_number'])
#                 print(ch['text'])
#                 print(ch['x0'])
#                 print(ch['bottom'])
#             res.append([float(ch['bottom']), col_loc, ch['page_number']])
#     else:
#         for ch in characs:
#             col_loc = 1
#             if ch['x0'] > 300:
#                 col_loc = 2
#             res.append([float(ch['bottom']), col_loc, ch['page_number']])
#
#     return res
#
#
# def get_parsed_txt(res, path, filename):
#     lim1, lim2, lim3, lim4 = 285, 285, 533, 538
#     pos1, pos2 = res[0][0], res[-1][0]
#     col_loc1, col_loc2 = res[0][1], res[-1][1]
#     npags = list(range(res[0][2], res[-1][2] + 1))
#     data = datetime.strptime(filename[4:14], '%Y-%m-%d')
#     data2 = datetime.strptime('2019-03-01', '%Y-%m-%d')
#     res1 = []
#     with pdfplumber.open(path + filename) as pdf:
#         texto = ''
#         lista = []
#         for count, p in enumerate(npags):
#             npage = p-1
#             page = pdf.pages[npage]
#             for c, linha in enumerate(page.lines):
#                 if c == 0:
#                     dist = float(linha['bottom'])
#                     break
#             page = page.filter(lambda x: float(x['bottom']) > dist)
#
#             try:
#                 tables = page.find_tables({
#                 "vertical_strategy": "lines",
#                 "horizontal_strategy": "explicit",
#                 "explicit_horizontal_lines": (page.curves + page.edges)})
#             except:
#                 tables = page.find_tables()
#
#
#             for tb in tables:
#                 tamanho = tb.bbox[2] - tb.bbox[0]
#                 if tamanho >= 465:
#                     lista.append([filename, npage])
#                     break
#     return lista
#
# def make_dfparsed(namedfpdfs, path):
#     start_pages = get_indexstartpages(namedfpdfs)
#     newdf = []
#     for key in tqdm(start_pages):
#         fname = key
#         startpg = start_pages[key]
#         result = get_location(startpg, path, fname)
#         parsed = get_parsed_txt(result, path, fname)
#         newdf.append(parsed)
#     return newdf
#
# def get_indexstartpages(namedfpdfs):
#     dfpdfs = read_csv(namedfpdfs, index_col='filename')
#     spages = dfpdfs['pages_summ'].dropna()
#     spages = spages.apply(literal_eval)
#     spages = dict(spages.apply(lambda x: int(x[0])))
#     return spages
#
#
# def column_page_col(dfparsed):
#     dfparsed['page_col'] = 0
#     pg = '0'
#     for row in dfparsed.iterrows():
#         txto = row[1][1]
#         if txto[:2] == '\n\n' and txto[6:8] == '\n\n':
#             pg = txto[:8]
#             pg = pg[2:-2]
#             txto = txto[8:]
#         try:
#             int(pg[:2])
#             dfparsed.loc[row[0], 'page_col'] = pg
#             dfparsed.loc[row[0], 'txt'] = txto
#             dfparsed = dfparsed[['filename', 'page_col', 'txt']]
#         except Exception as e:
#             print('PROBLEMA: 1 OU 3 DIGITOS NO NÚMERO DA PÁGINA')
#             print(e)
#             return False
#     return dfparsed
#
#
# # dire = 'arquivos_DOE/2018/'
# # fname = 'DOE_2018-11-09.pdf'
# # resu = get_location(36, dire, fname)
# # aa = get_parsed_txt(resu, dire, fname)
#
# yr = 2018
# path1 = f'arquivos_DOE/{yr}/'
#
# df = make_dfparsed(f'PDFs{yr}_index.csv', path1)
# print(len(df))
# print(df)

import pandas as pd
from ast import literal_eval
st = """[[], [], [], [], [], [['DOE_2018-01-12.pdf', 30]], [['DOE_2018-01-15.pdf', 70]], [], [], [], [], [], [['DOE_2018-01-24.pdf', 28]], [], [], [], [], [], [], [], [], [], [], [], [['DOE_2018-02-19.pdf', 19]], [], [['DOE_2018-02-28.pdf', 24]], [], [['DOE_2018-03-02.pdf', 27]], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [['DOE_2018-05-08.pdf', 20]], [], [], [], [], [['DOE_2018-05-15.pdf', 57]], [], [], [], [], [['DOE_2018-05-22.pdf', 26]], [], [], [], [['DOE_2018-05-29.pdf', 47]], [], [], [], [], [], [], [], [['DOE_2018-06-14.pdf', 22]], [], [], [], [['DOE_2018-06-20.pdf', 35]], [], [], [], [['DOE_2018-06-27.pdf', 31]], [['DOE_2018-06-28.pdf', 40]], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [['DOE_2018-07-27.pdf', 29]], [], [['DOE_2018-07-31.pdf', 27]], [], [['DOE_2018-08-02.pdf', 24]], [], [], [['DOE_2018-08-07.pdf', 146]], [], [], [], [['DOE_2018-08-13.pdf', 20]], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [['DOE_2018-09-10.pdf', 47]], [['DOE_2018-09-11.pdf', 239]], [], [], [], [['DOE_2018-09-17.pdf', 77], ['DOE_2018-09-17.pdf', 78]], [], [['DOE_2018-09-19.pdf', 39]], [], [['DOE_2018-09-21.pdf', 31]], [], [], [], [['DOE_2018-09-27.pdf', 34]], [['DOE_2018-09-28.pdf', 47]], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [['DOE_2018-11-09.pdf', 36]], [], [], [], [['DOE_2018-11-19.pdf', 28], ['DOE_2018-11-19.pdf', 29]], [], [], [], [['DOE_2018-11-26.pdf', 45]], [], [], [['DOE_2018-11-29.pdf', 29]], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]"""
st = st.replace('[], ', '').replace(', []', '')
st = st.replace('[[', '[').replace(']]', ']')
st = pd.DataFrame(literal_eval(st), columns=['fname', 'pg'])
print(len(st.fname.unique()))
print(st)
print(len(st))