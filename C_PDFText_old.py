from pandas import DataFrame, concat, read_csv
from os import listdir
from tqdm import tqdm
from PyPDF2 import PdfFileReader


class DiarioPDF:
    def __init__(self, path, filename):
        self.filename = filename
        self.pages_summ = None
        self.txts_summ = []
        self.pages_others = []
        self.txts_others = []
        self.info_others = []

        pdf = open(f'{path}{self.filename}', 'rb')
        self.pdf = PdfFileReader(pdf)

        self.npgs = self.pdf.numPages

    def create_summ_info(self):
        pg = self.pdf.getPage(0)
        txt = pg.extractText()
        pos = txt.find('INSTITUTO DE TERRAS DO PARÁ')
        if pos == -1:
            pos = txt.find('INSTITUTO DE TERRAS')
        if pos != -1:
            ntxt = txt[pos:].split('\n')[:3]
            ntxt = '\n'.join(ntxt)
            pag = [int(n) for n in ntxt.split() if n.isdigit()]
            pag = str(pag).replace('[', '').replace(']', '')

            pos2 = txt[pos:].find(pag) + 2
            ntxt2 = txt[pos + pos2:].split('\n')[:7]
            ntxt2 = '\n'.join(ntxt2)
            pag2 = [int(n) for n in ntxt2.split() if n.isdigit()]
            pag2 = pag2[0]
            pag2 = str(pag2).replace('[', '').replace(']', '')
            self.pages_summ = list(range(int(pag), int(pag2)+1))

            for pag in self.pages_summ:
                pag -= 1
                pag = self.pdf.getPage(pag)
                txt = pag.extractText()
                self.txts_summ.append(txt)

    def create_others(self):
        if self.pages_summ:
            listaps = self.pages_summ
        else:
            listaps = []

        for n in range(0, self.npgs):
            npagina = n + 1
            if npagina not in listaps:
                pag = self.pdf.getPage(n)
                txt = pag.extractText()
                if 'Instituto de Terras do Pará' in txt:
                    self.pages_others.append(npagina)
                    self.txts_others.append(txt)
                    self.info_others.append(0)
                if 'ITERPA' in txt:
                    self.pages_others.append(npagina)
                    self.txts_others.append(txt)
                    self.info_others.append(1)
                if ('ITERPA' not in txt) and ('iterpa' in txt.lower()):
                    self.pages_others.append(npagina)
                    self.txts_others.append(txt)
                    self.info_others.append(2)
                if ('Instituto de Terras do Pará' not in txt) and ('instituto de terras do pará' in txt.lower()):
                    self.pages_others.append(npagina)
                    self.txts_others.append(txt)
                    self.info_others.append(3)

    def create_list(self):
        lista = [self.filename, self.pages_summ, self.txts_summ,
                 self.pages_others, self.txts_others, self.info_others]
        return lista


def make_df(path, files):
    rows = []
    for file in tqdm(files):
        diario = DiarioPDF(path, file)
        diario.create_summ_info()
        diario.create_others()
        lista = diario.create_list()
        rows.append(lista)

    df = DataFrame(rows, columns=['filename', 'pages_summ', 'texts_summ', 'pages_others',
                                  'txts_others', 'info_others'])
    df.set_index('filename', inplace=True)
    return df


def update_df(path, dfname):
    lista = listdir(path)
    df = read_csv(dfname, index_col='filename')
    files_old = list(df.index)
    rows = []
    for file in tqdm(lista):
        if file not in files_old:
            diario = DiarioPDF(path, file)
            diario.update_summ_info()
            diario.update_others()
            lis = diario.make_list()
            rows.append(lis)

    if rows:
        df1 = DataFrame(rows, columns=['filename', 'pages_summ', 'texts_summ', 'pages_others',
                                       'txts_others', 'info_others'])
        df1.set_index('filename', inplace=True)
        df1 = concat([df, df1])
    else:
        df1 = False
    return df1

# path1 = 'arquivos_DOE/2020/'
# fn = 'DOE_2020-02-27.pdf'
# d = DiarioPDF(path1, fn)
# d.update_summ_info()
# print(d.pages_summ)

################## MAKE
yr = 2020
path1 = f'arquivos_DOE/{yr}/'
files = listdir(path1)
df1 = make_df(path1, files)
df1.to_csv(f'PDFs{yr}_index.csv')