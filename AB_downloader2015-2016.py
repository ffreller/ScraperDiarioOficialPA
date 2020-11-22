from Z0_defs import open_driver
from tqdm import tqdm
import urllib.request

ano = 2015
driver = open_driver()
driver.get(f'http://ioepa.com.br/arquivos/{ano}/')
elems = driver.find_elements_by_xpath("//a[@href]")
diretorio = r"C:\Users\Fabio Freller\Desktop\ScraperDiario\arquivos_DOE" + f'/{ano}'
for elem in tqdm(elems):
    linkpdf = elem.get_attribute("href")
    if linkpdf[-4:] == '.pdf':
        fname = f"/DOE_{linkpdf[34:44].replace('.', '-')}"
        if 'suplemento' in linkpdf:
            fname += '_suplemento'
        fname += ".pdf"
        urllib.request.urlretrieve(linkpdf, diretorio + fname)
driver.close()