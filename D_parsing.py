import pdfplumber
from pandas import read_csv, concat, DataFrame
from Z1_regex import parse_text, inconsistencias, corrigir_texto
from ast import literal_eval
from tqdm import tqdm
from datetime import datetime

year = 2015
# years = [2020, 2019, 2018, 2017, 2016, 2015]


def get_location(startpage, filename):
    characs = []
    pal = ''
    check1 = False
    check2 = False
    data = datetime.strptime(filename[4:14], '%Y-%m-%d')
    data2 = datetime.strptime('2019-03-01', '%Y-%m-%d')
    path = f'arquivos_DOE/{data.year}/'
    with pdfplumber.open(path + filename) as pdf:
        npage = startpage - 1
        if filename == 'DOE_2018-07-13.pdf':
            npage -= 1
        page = pdf.pages[npage]

        for c, cha in enumerate(page.chars):
            rsize = round(float(cha['width']) / float(cha['adv']))
            if check1:
                characs.append(cha)
                if rsize == 12:
                    check2 = True
                    break
            if not check1 and rsize == 12:
                pal += cha['text']
                if 'TERRAS DO PARÁ' in pal:
                    check1 = True

        while not check2:
            npage += 1
            page = pdf.pages[npage]
            for c, linha in enumerate(page.lines):
                if c == 0:
                    dist = float(linha['bottom'])
                    break
            if filename == 'DOE_2018-05-16.pdf' and npage == 38:
                dist = float(78)
            for c, cha in enumerate(page.chars):
                rsize = round(float(cha['width']) / float(cha['adv']))
                if float(cha['bottom']) > dist:
                    characs.append(cha)
                    if rsize == 12:
                        check2 = True
                        break

    res = []
    lim1, lim2, lim3, lim4 = 285, 285, 533, 534
    if data < data2:
        for ch in characs:
            col_loc = 0
            if float(ch['x0']) < lim1:
                col_loc = 1
            elif lim2 < float(ch['x0']) < lim3:
                col_loc = 2
            elif float(ch['x0']) > lim4:
                col_loc = 3
            # if col_loc == 0:
            #     print('Ainda com problema', filename, ch['page_number'])
            #     print(ch['text'])
            #     print(ch['x0'])
            #     print(ch['bottom'])
            res.append([float(ch['bottom']), col_loc, ch['page_number']])
    else:
        for ch in characs:
            col_loc = 1
            if ch['x0'] > 300:
                col_loc = 2
            res.append([float(ch['bottom']), col_loc, ch['page_number']])

    return res


def get_parsed_txt(res, filename):
    pos1, pos2 = res[0][0], res[-1][0]
    col_loc1, col_loc2 = res[0][1], res[-1][1]
    npags = list(range(res[0][2], res[-1][2] + 1))
    lim1, lim2, lim3, lim4 = 285, 285, 533, 533
    data = datetime.strptime(filename[4:14], '%Y-%m-%d')
    data2 = datetime.strptime('2019-03-01', '%Y-%m-%d')
    path = f'arquivos_DOE/{data.year}/'
    res1 = []
    listaproblemas = []
    with pdfplumber.open(path + filename) as pdf:
        texto = ''
        for count, p in enumerate(npags):
            p -= 1
            npage = p
            page = pdf.pages[npage]

            try:
                tables = page.find_tables({
                    "vertical_strategy": "lines",
                    "horizontal_strategy": "explicit",
                    "explicit_horizontal_lines": (page.curves + page.edges)})
            except:
                tables = page.find_tables()

            tabelagrande = False
            for tb in tables:
                tamanho = tb.bbox[2] - tb.bbox[0]
                if tamanho >= 350:
                    tabelagrande = True

            if tabelagrande:
                listaproblemas.append([filename, npage])
                continue

            for c, linha in enumerate(page.lines):
                if c == 0:
                    dist = float(linha['bottom'])
                    break
            page = page.filter(lambda x: float(x['bottom']) > dist)

            if data < data2:
                col1 = page.filter(lambda x: float(x['x0']) < lim1)
                col2 = page.filter(lambda x: lim2 < float(x['x0']) < lim3)
                col3 = page.filter(lambda x: float(x['x0']) > lim4)

                if count == 0:
                    if len(npags) == 1:
                        if col_loc1 == 1 and col_loc2 == 1:
                            col1 = col1.filter(lambda x: float(x['bottom']) > pos1)
                            col1 = col1.filter(lambda x: float(x['bottom']) < pos2)
                            col1 = col1.extract_text()
                            txt = f'\n\n{npage + 1}||1\n\n' + col1
                        elif col_loc1 == 2 and col_loc2 == 2:
                            col2 = col2.filter(lambda x: float(x['bottom']) > pos1)
                            col2 = col2.filter(lambda x: float(x['bottom']) < pos2)
                            col2 = col2.extract_text()
                            txt = f'\n\n{npage + 1}||2\n\n' + col2
                        elif col_loc1 == 3 and col_loc2 == 3:
                            col3 = col3.filter(lambda x: float(x['bottom']) > pos1)
                            col3 = col3.filter(lambda x: float(x['bottom']) < pos2)
                            col3 = col3.extract_text()
                            txt = f'\n\n{npage + 1}||3\n\n' + col3
                        elif col_loc1 == 1 and col_loc2 == 2:
                            col1 = col1.filter(lambda x: float(x['bottom']) > pos1)
                            col2 = col2.filter(lambda x: float(x['bottom']) < pos2)
                            col1 = col1.extract_text()
                            col2 = col2.extract_text()
                            if col2 is not None:
                                txt = f'\n\n{npage + 1}||1\n\n' + col1 + f'\n\n{npage + 1}||2\n\n' + col2
                            else:
                                txt = f'\n\n{npage + 1}||1\n\n' + col1
                        elif col_loc1 == 1 and col_loc2 == 3:
                            col1 = col1.filter(lambda x: float(x['bottom']) > pos1)
                            col3 = col3.filter(lambda x: float(x['bottom']) < pos2)
                            col1 = col1.extract_text()
                            col2 = col2.extract_text()
                            col3 = col3.extract_text()
                            if col3 is not None:
                                txt = f'\n\n{npage + 1}||1\n\n' + col1 + f'\n\n{npage + 1}||2\n\n' + col2 + \
                                      f'\n\n{npage + 1}||3\n\n' + col3
                            else:
                                txt = f'\n\n{npage + 1}||1\n\n' + col1 + f'\n\n{npage + 1}||2\n\n' + col2
                        elif col_loc1 == 2 and col_loc2 == 3:
                            col2 = col2.filter(lambda x: float(x['bottom']) > pos1)
                            col3 = col3.filter(lambda x: float(x['bottom']) < pos2)
                            col2 = col2.extract_text()
                            col3 = col3.extract_text()
                            if col3 is not None:
                                txt = f'\n\n{npage + 1}||2\n\n' + col2 + f'\n\n{npage + 1}||3\n\n' + col3
                            else:
                                txt = f'\n\n{npage + 1}||2\n\n' + col2

                    else:
                        if col_loc1 == 1:
                            col1 = col1.filter(lambda x: float(x['bottom']) > pos1)
                            col1 = col1.extract_text()
                            col2 = col2.extract_text()
                            col3 = col3.extract_text()
                            txt = f'\n\n{npage + 1}||1\n\n' + col1 + f'\n\n{npage + 1}||2\n\n' + col2 + \
                                  f'\n\n{npage + 1}||3\n\n' + col3
                        elif col_loc1 == 2:
                            col2 = col2.filter(lambda x: float(x['bottom']) > pos1)
                            col2 = col2.extract_text()
                            col3 = col3.extract_text()
                            txt = f'\n\n{npage + 1}||2\n\n' + col2 + f'\n\n{npage + 1}||3\n\n' + col3
                        elif col_loc1 == 3:
                            col3 = col3.filter(lambda x: float(x['bottom']) > pos1)
                            col3 = col3.extract_text()
                            txt = f'\n\n{npage + 1}||3\n\n' + col3

                elif count == (len(npags) - 1):
                    if col_loc2 == 1:
                        col1 = col1.filter(lambda x: float(x['bottom']) < pos2)
                        col1 = col1.extract_text()
                        if col1 is not None:
                            txt = f'\n\n{npage + 1}||1\n\n' + col1
                        else:
                            txt = ''
                    elif col_loc2 == 2:
                        col2 = col2.filter(lambda x: float(x['bottom']) < pos2)
                        col1 = col1.extract_text()
                        col2 = col2.extract_text()
                        if col2 is not None:
                            txt = f'\n\n{npage + 1}||1\n\n' + col1 + f'\n\n{npage + 1}||2\n\n' + col2
                        else:
                            txt = f'\n\n{npage + 1}||1\n\n' + col1
                    elif col_loc2 == 3:
                        col3 = col3.filter(lambda x: float(x['bottom']) < pos2)
                        col1 = col1.extract_text()
                        col2 = col2.extract_text()
                        col3 = col3.extract_text()
                        if col3 is not None:
                            txt = f'\n\n{npage + 1}||1\n\n' + col1 + f'\n\n{npage + 1}||2\n\n' + col2 + \
                                  f'\n\n{npage + 1}||3\n\n' + col3
                        else:
                            txt = f'\n\n{npage + 1}||1\n\n' + col1 + f'\n\n{npage + 1}||2\n\n' + col2

                else:
                    col1 = col1.extract_text()
                    col2 = col2.extract_text()
                    col3 = col3.extract_text()
                    txt = f'\n\n{npage + 1}||1\n\n' + col1 + f'\n\n{npage + 1}||2\n\n' + col2 + \
                          f'\n\n{npage + 1}||3\n\n' + col3

            else:
                col1 = page.filter(lambda x: float(x['x0']) < 300)
                col2 = page.filter(lambda x: float(x['x0']) > 300)

                if count == 0:
                    if len(npags) == 1:
                        if col_loc1 == 2 and col_loc2 == 2:
                            col2 = col2.filter(lambda x: float(x['bottom']) > pos1)
                            col2 = col2.filter(lambda x: float(x['bottom']) < pos2)
                            col2 = col2.extract_text()
                            txt = f'\n\n{npage + 1}||2\n\n' + col2

                        elif col_loc1 == 1 and col_loc2 == 2:
                            col1 = col1.filter(lambda x: float(x['bottom']) > pos1)
                            col2 = col2.filter(lambda x: float(x['bottom']) < pos2)
                            col1 = col1.extract_text()
                            col2 = col2.extract_text()
                            if col2 is not None:
                                txt = f'\n\n{npage + 1}||1\n\n' + col1 + f'\n\n{npage + 1}||2\n\n' + col2
                            else:
                                txt = f'\n\n{npage + 1}||1\n\n' + col1

                        elif col_loc1 == 1 and col_loc2 == 1:
                            col1 = col1.filter(lambda x: float(x['bottom']) > pos1)
                            col1 = col1.filter(lambda x: float(x['bottom']) < pos2)
                            col1 = col1.extract_text()
                            txt = f'\n\n{npage + 1}||1\n\n' + col1
                    else:
                        if col_loc1 == 2:
                            col2 = col2.filter(lambda x: float(x['bottom']) > pos1)
                            col2 = col2.extract_text()
                            txt = f'\n\n{npage + 1}||2\n\n' + col2
                        else:
                            col1 = col1.filter(lambda x: float(x['bottom']) > pos1)
                            col1 = col1.extract_text()
                            col2 = col2.extract_text()
                            txt = f'\n\n{npage + 1}||1\n\n' + col1 + f'\n\n{npage + 1}||2\n\n' + col2

                elif count == (len(npags) - 1):
                    if col_loc2 == 2:
                        col2 = col2.filter(lambda x: float(x['bottom']) < pos2)
                        col1 = col1.extract_text()
                        col2 = col2.extract_text()
                        if col2 is not None:
                            txt = f'\n\n{npage + 1}||1\n\n' + col1 + f'\n\n{npage + 1}||2\n\n' + col2
                        else:
                            txt = f'\n\n{npage + 1}||1\n\n' + col1

                    else:
                        col1 = col1.filter(lambda x: float(x['bottom']) < pos2)
                        col1 = col1.extract_text()
                        if col1 is not None:
                            txt = f'\n\n{npage + 1}||1\n\n' + col1
                        else:
                            txt = ''

                else:
                    col1 = col1.extract_text()
                    col2 = col2.extract_text()
                    txt = f'\n\n{npage + 1}||1\n\n' + col1 + f'\n\n{npage + 1}||2\n\n' + col2
            try:
                # if filename == 'DOE_2018-05-16.pdf':
                #     if txt.find('NÚCLEO DE') != -1:
                #         txt = txt[:txt.find('NÚCLEO DE')]
                #         txt += ""
                texto += txt
            except Exception as e:
                print(e)
                print(filename, npage, col_loc1, col_loc2)

    ress = parse_text(texto)

    for re1 in ress:
        re1 = inconsistencias(re1)
        for re2 in re1:
            re2 = inconsistencias(re2)
            for re3 in re2:
                re3 = inconsistencias(re3)
                for r in re3:
                    # print('indo')
                    res1.append([filename, r])

    return res1, listaproblemas


def get_indexstartpages(yr):
    dfpdfs = read_csv(f'PDFs{yr}_index.csv', index_col='filename')
    spages = dfpdfs['pages_summ'].dropna()
    spages = spages.apply(literal_eval)
    spages = dict(spages.apply(lambda x: int(x[0])))
    return spages


def make_dfparsed(yr):
    print(yr)
    start_pages = get_indexstartpages(yr)
    newdf = []
    dfproblemas = []
    for key in tqdm(start_pages):
        fname = key
        startpg = start_pages[key]
        result = get_location(startpg, fname)
        parsed, listaproblemas = get_parsed_txt(result, fname)
        for row in parsed:
            newdf.append(row)
        if listaproblemas:
            for row in listaproblemas:
                dfproblemas.append(row)

    newdf = DataFrame(newdf, columns=['filename', 'txt'])
    newdf['txt'] = newdf['txt'].apply(corrigir_texto)
    newdf.to_csv(f'parsed{yr}.csv')

    dfproblemas = DataFrame(dfproblemas, columns=['filename', 'page'])
    dfproblemas.to_csv(f'problemas{yr}.csv')
    return newdf


def update_dfparsed(yr):
    start_pages = get_indexstartpages(yr)
    df = read_csv(f'parsed{yr}.csv')
    pdfs_old = list(df['filename'].unique())
    newdf = []
    for key in tqdm(start_pages):
        fname = key
        if fname not in pdfs_old:
            startpg = start_pages[key]
            result = get_location(startpg, fname)
            parsed, listaproblemas = get_parsed_txt(result, fname)
            for row in parsed:
                newdf.append(row)

    if newdf:
        df1 = DataFrame(newdf, columns=['filename', 'txt'])
        df1['txt'] = df1['txt'].apply(corrigir_texto)
        df1 = concat([df, df1])
    else:
        df1 = False
    return df1


# ndf = make_dfparsed(year)
# print(len(ndf))

# for year in years:
#     ndf = make_dfparsed(year)
#     # CORRIGINDO PROBLEMA ##############################
#     if year == 2017:
#         txt0 = ndf[ndf['txt'].str.contains('portaria nº 0614/2017')]['txt'].iloc[0]
#         finame = ndf[ndf['txt'].str.contains('portaria nº 0614/2017')]['filename'].iloc[0]
#         txts = txt0.split('portaria nº 0614/2017')
#         novotexto = 'portaria nº 0614/2017'+txts[1]
#         ndf[ndf['txt'].str.contains('portaria nº 0614/2017')] = txts[0]
#         novarow = {'filename': finame, 'txt': novotexto}
#         ndf = ndf.append(novarow, ignore_index=True)
#     #####################################
#
#     ndf.to_csv(f'parsed{year}.csv')
