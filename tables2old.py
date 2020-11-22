from pandas import read_csv, concat
import difflib

def fuzzy_merge(df1, df2, left_on, right_on, how='inner', cutoff=0.6):
    df_other= df2.copy()
    df_other[left_on] = [get_closest_match(x, df1[left_on], cutoff)
                         for x in df_other[right_on]]
    return df1.merge(df_other, on=left_on, how=how)

def get_closest_match(x, other, cutoff):
    matches = difflib.get_close_matches(x, other, cutoff=cutoff)
    return matches[0] if matches else None


df_categorizado = read_csv('categorizado2020.csv', index_col='Unnamed: 0')
df_categorizado['txtlowerclass'] = df_categorizado['txt'].apply(lambda x: x.lower())
df_categorizado['txtlowerclass'] = df_categorizado['txtlowerclass'].apply(lambda x: x.replace('\n', ' '))
df_categorizado['txtlowerclass'] = df_categorizado['txtlowerclass'].apply(lambda x: x[1:] if x[0] == ' ' else x)
df_categorizado['txtlowerclass'] = df_categorizado['txtlowerclass'].apply(lambda x: x[1:] if x[0] == ' ' else x)
print('Tamanho começo:', len(df_categorizado))


df_appended = read_csv('appended2020.csv', index_col='0')
df_appended['txtlower'] = df_appended['txtlower'].apply(lambda x: x.replace('\\n', ' ').replace('..', ''))
df_appended['txtlower'] = df_appended['txtlower'].apply(lambda x: x[1:] if x[0] == ' ' else x)
df_appended['txtlower'] = df_appended['txtlower'].apply(lambda x: x[1:] if x[0] == ' ' else x)
df_appended['txtlower'] = df_appended['txtlower'].apply(lambda x: x[:x.find('doe_20')] if 'doe_20' in x else x)


merged = df_appended.merge(df_categorizado, right_on='txtlowerclass', left_on='txtlower', how='outer')
erros = merged[merged['classificacao'].isna()]
erros = erros[['table', 'filename_y', 'page', 'col', 'tamanho', 'texto_sel', 'score', 'txtlower']]
merged = merged[['filename_y', 'txt', 'table', 'page', 'col', 'tamanho', 'texto_sel', 'score','classificacao']]
merged.rename(columns={'filename_y': 'filename'}, inplace=True)


df2 = fuzzy_merge(df_categorizado, erros, left_on='txtlowerclass', right_on='txtlower', how='right')

df2.columns
df2 = df2[['filename', 'txt', 'table', 'page', 'col', 'tamanho', 'texto_sel', 'score','classificacao']]

merged = merged[merged['classificacao'].isna() == False]

finaldf = concat([merged, df2])
finaldf = finaldf[['filename', 'txt', 'table', 'classificacao']]

print('Tamanho final:', len(finaldf))

# print(len(finaldf))
# finaldf.drop_duplicates(subset='txt', inplace=True)
# print(len(finaldf))

finaldf.to_csv('tabelas_categorizado.csv')
finaldf.to_pickle('tabelas_categorizado.pickle')