import pdfplumber
from pandas import DataFrame, read_csv, read_pickle
from Z1_regex import corrigir_texto
from D_parsing import get_indexstartpages, get_location, get_parsed_txt
from tqdm import tqdm
import difflib
from datetime import datetime
from os import listdir

years = [2016, 2015]
# years = [2020, 2019, 2018, 2017, 2016, 2015]


def fuzzy_merge(df1, df2, left_on, right_on, how='inner', cutoff=0.8):
    df_other = df2.copy()
    df_other[left_on] = [get_closest_match(x, df1[left_on], cutoff)
                         for x in df_other[right_on]]
    return df1.merge(df_other, on=left_on, how=how)


def get_closest_match(x, other, cutoff):
    matches = difflib.get_close_matches(x, other, cutoff=cutoff)
    return matches[0] if matches else None


def choose_text(row):
    best_score = 0
    tabela = row['table']
    fname_textos = row['txts'][0]
    textos = [x[1] for x in fname_textos]
    texto_sel = ""
    if len(textos) != 0:
        for texto in textos:
            score = 0
            lenlista = 0
            for linha in tabela:
                for element in linha:
                    if element:
                        listapalavras = element.split(' ')
                        lenlista += len(listapalavras)
                        for palavra in listapalavras:
                            if texto.lower().find(palavra.lower()) != -1:
                                score += 1
            if lenlista != 0:
                score = score/lenlista
            else:
                score = 0
                print(row['filename'])
            if score > best_score:
                best_score = score
                texto_sel = texto
        return [best_score, texto_sel]
    else:
        print('*'*50)
        print('Erro: sem texto')
        print(row)
        print('*'*50)
        return [0, 'ERRO']


def tables_from_col(col, filename, npage, col12):
    res = []
    try:
        tabelas_obj = col.find_tables({
            "vertical_strategy": "lines",
            "horizontal_strategy": "explicit",
            "explicit_horizontal_lines": (col.curves + col.edges)})
    except:
        tabelas_obj = col.find_tables()
    if len(tabelas_obj) > 0:
        for tabela_obj in tabelas_obj:
            tabela = tabela_obj.extract()
            bbox = tabela_obj.bbox
            res.append([filename, npage+1, col12, tabela, bbox])
        return res
    else:
        pass


def get_tables(res, filename):
    lim1, lim2, lim3, lim4 = 285, 285, 533, 538
    pos1, pos2 = res[0][0], res[-1][0]
    col_loc1, col_loc2 = res[0][1], res[-1][1]
    npags = list(range(res[0][2], res[-1][2] + 1))
    data = datetime.strptime(filename[4:14], '%Y-%m-%d')
    data2 = datetime.strptime('2019-03-01', '%Y-%m-%d')
    path = f'arquivos_DOE/{data.year}/'
    res1 = []
    with pdfplumber.open(path + filename) as pdf:
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
                continue

            if len(tables) != 0:
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
                                tb = tables_from_col(col1, filename, npage, 1)
                                if tb:
                                    for t in tb:
                                        res1.append(t)

                            elif col_loc1 == 2 and col_loc2 == 2:
                                col2 = col2.filter(lambda x: float(x['bottom']) > pos1)
                                col2 = col2.filter(lambda x: float(x['bottom']) < pos2)
                                tb = tables_from_col(col2, filename, npage, 2)
                                if tb:
                                    for t in tb:
                                        res1.append(t)

                            elif col_loc1 == 3 and col_loc2 == 3:
                                col3 = col3.filter(lambda x: float(x['bottom']) > pos1)
                                col3 = col3.filter(lambda x: float(x['bottom']) < pos2)
                                tb = tables_from_col(col3, filename, npage, 3)
                                if tb:
                                    for t in tb:
                                        res1.append(t)

                            elif col_loc1 == 1 and col_loc2 == 2:
                                col1 = col1.filter(lambda x: float(x['bottom']) > pos1)
                                tb1 = tables_from_col(col1, filename, npage, 1)
                                if tb1:
                                    for t in tb1:
                                        res1.append(t)

                                col2 = col2.filter(lambda x: float(x['bottom']) < pos2)
                                tb2 = tables_from_col(col2, filename, npage, 2)
                                if tb2:
                                    for t in tb2:
                                        res1.append(t)

                            elif col_loc1 == 1 and col_loc2 == 3:
                                col1 = col1.filter(lambda x: float(x['bottom']) > pos1)
                                tb1 = tables_from_col(col1, filename, npage, 1)
                                if tb1:
                                    for t in tb1:
                                        res1.append(t)

                                tb2 = tables_from_col(col2, filename, npage, 2)
                                if tb2:
                                    for t in tb2:
                                        res1.append(t)

                                col3 = col3.filter(lambda x: float(x['bottom']) < pos2)
                                tb3 = tables_from_col(col3, filename, npage, 3)
                                if tb3:
                                    for t in tb3:
                                        res1.append(t)

                            elif col_loc1 == 2 and col_loc2 == 3:
                                col2 = col2.filter(lambda x: float(x['bottom']) > pos1)
                                tb2 = tables_from_col(col2, filename, npage, 2)
                                if tb2:
                                    for t in tb2:
                                        res1.append(t)

                                col3 = col3.filter(lambda x: float(x['bottom']) < pos2)
                                tb3 = tables_from_col(col3, filename, npage, 3)
                                if tb3:
                                    for t in tb3:
                                        res1.append(t)
                        else:
                            if col_loc1 == 1:
                                col1 = col1.filter(lambda x: float(x['bottom']) > pos1)
                                tb1 = tables_from_col(col1, filename, npage, 1)
                                if tb1:
                                    for t in tb1:
                                        res1.append(t)

                                tb2 = tables_from_col(col2, filename, npage, 2)
                                if tb2:
                                    for t in tb2:
                                        res1.append(t)

                                tb3 = tables_from_col(col3, filename, npage, 3)
                                if tb3:
                                    for t in tb3:
                                        res1.append(t)

                            elif col_loc1 == 2:
                                col2 = col2.filter(lambda x: float(x['bottom']) > pos1)
                                tb2 = tables_from_col(col2, filename, npage, 2)
                                if tb2:
                                    for t in tb2:
                                        res1.append(t)

                                tb3 = tables_from_col(col3, filename, npage, 3)
                                if tb3:
                                    for t in tb3:
                                        res1.append(t)

                            elif col_loc1 == 3:
                                col3 = col3.filter(lambda x: float(x['bottom']) > pos1)
                                tb3 = tables_from_col(col3, filename, npage, 3)
                                if tb3:
                                    for t in tb3:
                                        res1.append(t)

                    elif count == (len(npags) - 1):
                        if col_loc2 == 1:
                            col1 = col1.filter(lambda x: float(x['bottom']) < pos2)
                            tb = tables_from_col(col1, filename, npage, 1)
                            if tb:
                                for t in tb:
                                    res1.append(t)

                        elif col_loc2 == 2:
                            tb1 = tables_from_col(col1, filename, npage, 1)
                            if tb1:
                                for t in tb1:
                                    res1.append(t)

                            col2 = col2.filter(lambda x: float(x['bottom']) < pos2)
                            tb2 = tables_from_col(col2, filename, npage, 2)
                            if tb2:
                                for t in tb2:
                                    res1.append(t)

                        elif col_loc2 == 3:
                            tb1 = tables_from_col(col1, filename, npage, 1)
                            if tb1:
                                for t in tb1:
                                    res1.append(t)

                            tb2 = tables_from_col(col2, filename, npage, 2)
                            if tb2:
                                for t in tb2:
                                    res1.append(t)

                            col3 = col3.filter(lambda x: float(x['bottom']) < pos2)
                            tb3 = tables_from_col(col3, filename, npage, 3)
                            if tb3:
                                for t in tb3:
                                    res1.append(t)

                    else:
                        tb1 = tables_from_col(col1, filename, npage, 1)
                        if tb1:
                            for t in tb1:
                                res1.append(t)

                        tb2 = tables_from_col(col2, filename, npage, 2)
                        if tb2:
                            for t in tb2:
                                res1.append(t)

                        tb3 = tables_from_col(col3, filename, npage, 3)
                        if tb3:
                            for t in tb3:
                                res1.append(t)

                else:
                    col1 = page.filter(lambda x: float(x['x0']) < 300)
                    col2 = page.filter(lambda x: float(x['x0']) > 300)
                    if count == 0:
                        if len(npags) == 1:
                            if col_loc1 == 2 and col_loc2 == 2:
                                col2 = col2.filter(lambda x: float(x['bottom']) > pos1)
                                col2 = col2.filter(lambda x: float(x['bottom']) < pos2)
                                tb = tables_from_col(col2, filename, npage, 2)
                                if tb:
                                    for t in tb:
                                        res1.append(t)

                            elif col_loc1 == 1 and col_loc2 == 2:
                                col1 = col1.filter(lambda x: float(x['bottom']) > pos1)
                                tb1 = tables_from_col(col1, filename, npage, 1)
                                if tb1:
                                    for t in tb1:
                                        res1.append(t)

                                col2 = col2.filter(lambda x: float(x['bottom']) < pos2)
                                tb2 = tables_from_col(col2, filename, npage, 2)
                                if tb2:
                                    for t in tb2:
                                        res1.append(t)

                            elif col_loc1 == 1 and col_loc2 == 1:
                                col1 = col1.filter(lambda x: float(x['bottom']) > pos1)
                                col1 = col1.filter(lambda x: float(x['bottom']) < pos2)
                                tb = tables_from_col(col1, filename, npage, 1)
                                if tb:
                                    for t in tb:
                                        res1.append(t)
                        else:
                            if col_loc1 == 2:
                                col2 = col2.filter(lambda x: float(x['bottom']) > pos1)
                                tb = tables_from_col(col2, filename, npage, 2)
                                if tb:
                                    for t in tb:
                                        res1.append(t)

                            else:
                                col1 = col1.filter(lambda x: float(x['bottom']) > pos1)
                                tb1 = tables_from_col(col1, filename, npage, 1)
                                if tb1:
                                    for t in tb1:
                                        res1.append(t)

                                tb2 = tables_from_col(col2, filename, npage, 2)
                                if tb2:
                                    for t in tb2:
                                        res1.append(t)

                    elif count == (len(npags) - 1):
                        if col_loc2 == 2:
                            tb1 = tables_from_col(col1, filename, npage, 1)
                            if tb1:
                                for t in tb1:
                                    res1.append(t)

                            col2 = col2.filter(lambda x: float(x['bottom']) < pos2)
                            tb2 = tables_from_col(col2, filename, npage, 2)
                            if tb2:
                                for t in tb2:
                                    res1.append(t)

                        else:
                            col1 = col1.filter(lambda x: float(x['bottom']) < pos2)
                            tb = tables_from_col(col1, filename, npage, 1)
                            if tb:
                                for t in tb:
                                    res1.append(t)

                    else:
                        tb1 = tables_from_col(col1, filename, npage, 1)
                        if tb1:
                            for t in tb1:
                                res1.append(t)

                        tb2 = tables_from_col(col2, filename, npage, 2)
                        if tb2:
                            for t in tb2:
                                res1.append(t)
    return res1


def criar_dftabela(yr):
    yr = str(yr)
    print('Criando nova tabela')
    d = read_csv(f'categorizado{yr}.csv')
    d['txt'] = d['txt'].apply(lambda x: x.lower())

    start_pages = get_indexstartpages(yr)
    lista = []
    for key in tqdm(start_pages):
        fname = key
        startpg = start_pages[key]
        pgs = get_location(startpg, fname)
        txs = get_parsed_txt(pgs, fname)
        tbs = get_tables(pgs, fname)
        for tb in tbs:
            lista.append([tb[0], tb[1], tb[2], tb[3], tb[4], txs])

    df = DataFrame(lista, columns=['filename', 'page', 'col', 'table', 'bbox', 'txts'])
    df.to_csv(f'tables{yr}.csv')
    df.to_pickle(f'tables{yr}.pickle')
    return df


def append_tables(df):
    lis = []
    i = 0
    rows = list(df.iterrows())
    while i < len(rows):
        row = rows[i][1]
        table, filename, page, col, txts = row[3], row[0], row[1], row[2], row[5]
        tamanho = 1
        while i < (len(rows) - 1):
            bbox_row = row['bbox']
            bottom_row = float(bbox_row[3])
            if bottom_row <= 808 or bottom_row >= 843:
                # old 811 814
                # checar 2020-07-29, 2020-09-03, 2019-01-15, 2019-02-14, 2019-04-23
                break

            row = rows[i][1]
            prox = rows[i + 1][1]

            if prox['filename'] != row['filename']:
                break

            if row['col'] == 1:
                if prox['page'] != row['page']:
                    break
                if prox['col'] == 1:
                    break
            else:
                if prox['page'] != (row['page'] + 1):
                    break

            bbox_prox = prox['bbox']
            top_prox = float(bbox_prox[1])

            if top_prox < 35 or top_prox > 90:
                break

            i += 1
            tamanho += 1
            table += prox.table
            txts += prox.txts
        lis.append([i, table, filename, page, col, tamanho, txts])

        i += 1

    df = DataFrame(lis)
    df.set_index(0, inplace=True)
    df.rename(columns={1: 'table', 2: 'filename', 3: 'page', 4: 'col', 5: 'tamanho', 6: 'txts'}, inplace=True)
    return df


for year in years:
    print(year)
    again = True
    if f'tables{year}.pickle'not in listdir() or again:
        df0 = criar_dftabela(year)
    else:
        df0 = read_pickle(f'tables{year}.pickle')

    print('Antes do append:', len(df0))
    df0 = append_tables(df0)
    print('Depois do append:', len(df0))

    df0['texto_sel'] = df0.apply(choose_text, axis=1)
    df0['score'] = df0['texto_sel'].apply(lambda x: x[0])
    df0['texto_sel'] = df0['texto_sel'].apply(lambda x: x[1])
    df0['texto_sel'] = df0['texto_sel'].apply(corrigir_texto)
    df0['txtlower'] = df0['texto_sel'].apply(lambda x: x.lower())
    print('Tamanho final:', len(df0))
    df0.to_csv(f'appended{year}.csv')
    print('*'*50)
    print()
