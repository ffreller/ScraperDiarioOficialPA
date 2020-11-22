from pandas import DataFrame, concat, read_csv
from os import listdir
from tqdm import tqdm
from datetime import datetime
from PyPDF2 import PdfFileReader
import pdfplumber

year = 2015
# years = [2015, 2016, 2017, 2018, 2019, 2020]


class DiarioPDF:
    def __init__(self, filename):
        yr = int(filename[4:8])
        self.path = f'arquivos_DOE/{yr}/'
        self.filename = filename
        self.data = datetime.strptime(self.filename[4:14], '%Y-%m-%d')
        self.pages_summ = None
        self.txts_summ = []
        self.pages_others = []
        self.txts_others = []
        self.info_others = []
        self.pagina_pular = 0

        pdf = open(f'{self.path}{self.filename}', 'rb')
        self.pdf = PdfFileReader(pdf, strict=False)
        self.npgs = self.pdf.numPages

    def create_summ_info(self):
        data1 = datetime.strptime('2019-01-07', '%Y-%m-%d')
        data2 = datetime.strptime('2019-03-01', '%Y-%m-%d')

        if self.data < data1:
            npg = 2
            self.pagina_pular = npg + 1
        elif data1 <= self.data < data2:
            npg = 0
            self.pagina_pular = npg + 1
        else:
            npg = 0
            self.pagina_pular = npg + 2

        if self.filename == "DOE_2018-07-25.pdf":
            npg = 10

        pg = self.pdf.getPage(npg)
        txt = pg.extractText()

        if txt.count('\n')/len(txt) > 0.1:
            print("Usando Pdfplumber.", self.filename)
            with pdfplumber.open(self.path + self.filename) as pdf:
                pg = pdf.pages[npg]
                txt = pg.extract_text()
                nesta_edicao = txt.find("NESTA EDIÇÃO")
                if "suplemento" not in self.filename and "EXTRA" not in self.filename and txt.count(".") < 500:
                    while nesta_edicao == -1 and npg <= 3 and txt.count(".") < 500:
                        print('Procurando o index', self.filename, "Página", npg+1)
                        npg += 1
                        self.pagina_pular += 1
                        pg = pdf.pages[npg]
                        txt = pg.extract_text()
                        nesta_edicao = txt.find("NESTA EDIÇÃO")

                pos = txt.find('INSTITUTO DE TERRAS DO PARÁ')
                if pos == -1:
                    pos = txt.find('INSTITUTO DE TERRAS')
                if pos != -1:
                    ntxt = txt[pos:].split('\n')[:8]
                    ntxt = '\n'.join(ntxt)
                    pag = [int(n) for n in ntxt.split() if n.isdigit()][:2]
                    if self.filename == 'DOE_2016-02-12.pdf':
                        self.pages_summ = list(range(22, 22 + 1))
                    elif self.filename == 'DOE_2020-02-27.pdf':
                        self.pages_summ = list(range(11, 11 + 1))
                    elif self.filename == 'DOE_2015-06-11.pdf':
                        self.pages_summ = list(range(29, 29 + 1))
                    else:
                        self.pages_summ = list(range(pag[0], pag[1] + 1))

                    for pag in self.pages_summ:
                        pag -= 1
                        pg = pdf.pages[npg]
                        txt = pg.extract_text()
                        self.txts_summ.append(txt)

        else:
            nesta_edicao = txt.find("NESTA EDIÇÃO")
            if ("suplemento" not in self.filename) and ("EXTRA" not in self.filename) and (txt.count(".") < 500):
                while nesta_edicao == -1 and npg <= 3 and txt.count(".") < 500:
                    print('Procurando o index', self.filename, "Página", npg+1)
                    npg += 1
                    self.pagina_pular += 1
                    pg = self.pdf.getPage(npg)
                    txt = pg.extractText()
                    nesta_edicao = txt.find("NESTA EDIÇÃO")

            pos = txt.find('INSTITUTO DE TERRAS DO PARÁ')
            if pos == -1:
                pos = txt.find('INSTITUTO DE TERRAS')
            if pos != -1 and self.filename != 'DOE_2015-10-01.pdf':
                ntxt = txt[pos:].split('\n')[:8]
                ntxt = '\n'.join(ntxt)
                pag = [int(n) for n in ntxt.split() if n.isdigit()][:2]
                if self.filename == 'DOE_2016-02-12.pdf':
                    self.pages_summ = list(range(22, 22 + 1))
                else:
                    self.pages_summ = list(range(pag[0], pag[1] + 1))

                for pag in self.pages_summ:
                    pag -= 1
                    pag = self.pdf.getPage(pag)
                    txt = pag.extractText()
                    self.txts_summ.append(txt)

            elif self.filename == 'DOE_2015-10-01.pdf':
                self.pages_summ = list(range(21, 22 + 1))
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
            if npagina not in listaps and n != self.pagina_pular:
                pag = self.pdf.getPage(n)
                try:
                    txt = pag.extractText()
                except Exception as e:
                    print(e)
                    print(self.filename, n)
                    txt = 'erro'
                if txt is not None:
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


def make_df(yr):
    print(yr)
    rows = []
    files = listdir(f'arquivos_DOE/{yr}/')
    for file in tqdm(files):
        try:
            diario = DiarioPDF(file)
        except Exception as e:
            print(1, file, e)
            continue
        try:
            diario.create_summ_info()
        except Exception as e:
            print(2, file, e)
            continue
        try:
            diario.create_others()
        except Exception as e:
            print(3, file, e)
            continue
        lista = diario.create_list()
        rows.append(lista)

    df = DataFrame(rows, columns=['filename', 'pages_summ', 'texts_summ', 'pages_others',
                                  'txts_others', 'info_others'])
    df.set_index('filename', inplace=True)
    df.to_csv(f'PDFs{yr}_index.csv')
    return df


def update_df(yr):
    lista = listdir(f'arquivos_DOE/{yr}/')
    df = read_csv(f'PDFs{yr}_index.csv', index_col='filename')
    files_old = list(df.index)
    rows = []
    for file in tqdm(lista):
        if file not in files_old:
            diario = DiarioPDF(file)
            diario.create_summ_info()
            diario.create_others()
            lis = diario.create_list()
            rows.append(lis)

    if rows:
        df1 = DataFrame(rows, columns=['filename', 'pages_summ', 'texts_summ', 'pages_others',
                                       'txts_others', 'info_others'])
        df1.set_index('filename', inplace=True)
        df1 = concat([df, df1])
    else:
        df1 = False
    return df1


# for year in years:
#     df0 = make_df(year)

df0 = make_df(year)
