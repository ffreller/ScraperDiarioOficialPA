from pandas import read_csv, concat
from Z1_regex import corrigir_texto, get_page
import difflib
import re

# year = 2015
years = [2021, 2020]


def fuzzy_merge(df1, df2, left_on, right_on, how='inner', cutoff=0.6):
    df_other = df2.copy()
    df_other[left_on] = [get_closest_match(x, df1[left_on], cutoff)
                         for x in df_other[right_on]]
    return df1.merge(df_other, on=left_on, how=how)


def get_closest_match(x, other, cutoff):
    matches = difflib.get_close_matches(x, other, cutoff=cutoff)
    return matches[0] if matches else None

def remove_pgcol(txt):
    patt = re.compile(' ? ?\d{2}_\d ? ?')
    if re.search(patt, txt):
        txt = re.sub(patt, '', txt)
    return txt


def get_final(yr):
    print(yr)
    df_categorizado = read_csv(f'categorizado{yr}.csv', index_col='Unnamed: 0')
    df_categorizado['txtlowerclass'] = df_categorizado['txt'].apply(lambda x: x.lower())
    df_categorizado['txtlowerclass'] = df_categorizado['txtlowerclass'].apply(lambda x: x.replace('\n', ' ').replace('..', ''))
    # df_categorizado['txtlowerclass'] = df_categorizado['txtlowerclass'].apply(remove_pgcol)
    df_categorizado['txtlowerclass'] = df_categorizado['txtlowerclass'].apply(lambda x: x[1:] if x[0] == ' ' else x)
    df_categorizado['txtlowerclass'] = df_categorizado['txtlowerclass'].apply(lambda x: x[1:] if x[0] == ' ' else x)
    df_categorizado['txtlowerclass'] = df_categorizado['txtlowerclass'].apply(corrigir_texto)
    print('Tamanho começo:', len(df_categorizado))

    df_appended = read_csv(f'appended{yr}.csv', index_col='0')
    df_appended = df_appended[df_appended['score'] != 0]

    # print('Antes de tirar os floats (df_appended):', len(df_appended))
    # print(df_appended[df_appended['txtlower'].apply(lambda x: isinstance(x, float))])
    # df_appended = df_appended[df_appended['txtlower'].apply(lambda x: isinstance(x, str))]
    # print('Depois de tirar os floats (df_appended):', len(df_appended))

    df_appended['txtorig'] = df_appended['txtlower']
    df_appended['txtlower'] = df_appended['txtlower'].apply(lambda x: x.replace('\n', ' ').replace('..', ''))
    # df_appended['txtlower'] = df_appended['txtlower'].apply(remove_pgcol)
    df_appended['txtlower'] = df_appended['txtlower'].apply(lambda x: x[1:] if x[0] == ' ' else x)
    df_appended['txtlower'] = df_appended['txtlower'].apply(lambda x: x[1:] if x[0] == ' ' else x)
    df_appended['txtlower'] = df_appended['txtlower'].apply(corrigir_texto)
    # df_appended['txtlower'] = df_appended['txtlower'].apply(lambda x: x[:x.find('doe_20')] if 'doe_20' in x else x)

    merged = df_appended.merge(df_categorizado, right_on='txtlowerclass', left_on='txtlower', how='outer')
    merged = merged[['filename_y', 'txt', 'table', 'page', 'col', 'tamanho', 'texto_sel', 'score', 'classificacao']]
    merged.rename(columns={'filename_y': 'filename'}, inplace=True)
    erros = merged[merged['classificacao'].isna()]
    merged = merged[merged['classificacao'].isna() == False]
    if len(erros) > 0:
        print('Erros:',len(erros))
        erros = erros[['table', 'filename_x', 'page', 'col', 'tamanho', 'texto_sel', 'score', 'txtlower']]
        merged2 = fuzzy_merge(df_categorizado, erros, left_on='txtlowerclass', right_on='txtlower', how='right')
        print('Fuzzy Merged!')
        merged2 = merged2[['filename', 'txt', 'table', 'page', 'col', 'tamanho', 'texto_sel', 'score', 'classificacao']]
        finaldf = concat([merged, merged2], ignore_index=True)
    else:
        finaldf = merged.copy()

    finaldf = finaldf[['filename', 'txt','score','table', 'classificacao']]

    print('Tamanho final:', len(finaldf))

    # print(finaldf[finaldf['txt'].apply(lambda x: isinstance(x, str) == False)])

    finaldf['txt'] = finaldf['txt'].apply(corrigir_texto)
    finaldf = get_page(finaldf)

    for column in finaldf.columns:
        finaldf[column] = finaldf[column].apply(lambda x: x.replace('\n', '') if type(x) == str else x)
        finaldf[column] = finaldf[column].apply(lambda x: x.replace('\\n', '') if type(x) == str else x)
        finaldf[column] = finaldf[column].apply(lambda x: x.replace('\n\r', '') if type(x) == str else x)
        # finaldf[column] = finaldf[column].apply(lambda x: x.replace('\n', '') if x is not None else x)

    finaldf.to_excel(f'tabelas_categorizado{yr}.xlsx')
    finaldf.to_pickle(f'tabelas_categorizado{yr}.pickle')

# get_final(year)

for year in years:
    get_final(year)
    print('*'*50)
