from datetime import timedelta, datetime, date
from os import remove
from time import sleep
from pathlib import Path
from pandas import read_csv
from google_drive_downloader import GoogleDriveDownloader as gdd


class Diario:
    def __init__(self, link, data):
        self.link = link
        self.data = data
        self.extra = False
        self.filename = f"/{self.data[:4]}/DOE_{self.data}.pdf"

        if self.link.split('=')[1] == 'sharing':
            id0 = self.link.split('/d/')[1]
            self.id0 = id0.split('/view')[0]
        else:
            self.id0 = self.link.split('=')[1]

    def set_extra(self):
        self.filename = self.filename[:-4] + "_EXTRA.pdf"
        self.extra = True

    def download(self, path):
        gdd.download_file_from_google_drive(file_id=self.id0, dest_path=path + self.filename, unzip=False)

    def is_corrupted(self, path):
        size = Path(path + self.filename).stat().st_size
        if size < 10000:
            hr = datetime.now() + timedelta(minutes=10)
            hr = hr.strftime("%H:%M")
            print(self.filename)
            print('Download failed')
            print('Next try:', hr)
            return True
        else:
            return False


def download_bydate(dflinks, path):
    for row in dflinks.iterrows():
        dt = row[0].replace('/', '-')

        for link in row[1]:
            if link != 'False':
                diario = Diario(link, dt)

                if link == row[1][1]:
                    diario.set_extra()

                diario.download(path)

                while diario.is_corrupted(path):
                    remove(path + diario.filename)
                    sleep(600)
                    diario.download(path)


df = read_csv('LinksDOE.csv', index_col='data')

today = date.today().strftime('%Y/%m/%d')
startdate = '2017/01/01'
enddate = '2017/12/31'
dfdts = df.loc[startdate:enddate]

download_bydate(dfdts, 'arquivos_DOE')