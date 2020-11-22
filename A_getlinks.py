from datetime import date, datetime
from tqdm import tqdm
from pandas import DataFrame, read_csv, concat, date_range, to_datetime
from Z0_defs import open_driver

def linksbypage(days):
    driver = open_driver()
    print('De: ', days[0].strftime("%d/%m/%Y"))
    print('Até: ', days[-1].strftime("%d/%m/%Y"))

    links = []
    for day in tqdm(days):
        day = day.strftime("%d/%m/%Y")
        driver.get(f'http://www.ioepa.com.br/Frame/?dts={day}')
        dt = driver.find_element_by_xpath('//*[@id="datepicker"]')
        dt = dt.get_attribute("value")
        link1, link2 = '', ''

        if day == dt:
            elems = driver.find_elements_by_xpath("//a[@href]")
            if len(elems) > 2:
                print('PROBLEMA: MAIS UM LINK')

            elif len(elems) > 1:
                link1 = elems[0].get_attribute("href")
                link2 = elems[1].get_attribute("href")

            else:
                link1 = elems[0].get_attribute("href")
                link2 = False

        else:
            link1 = False
            link2 = False

        day = datetime.strptime(day, '%d/%m/%Y').strftime('%Y/%m/%d')
        links.append([day, link1, link2])

    driver.quit()
    dflinks = DataFrame(links, columns=['data', 'link_DOE', 'link_DOE_EXTRA'])
    dflinks.set_index('data', inplace=True)
    return dflinks


def update_links(filename):
    dfold = read_csv(filename, index_col='data')
    olddates = to_datetime(dfold.index)
    startdate = olddates.max()

    today = date.today()
    days = date_range(startdate, today, freq='d')

    if len(days) != 0:
        newrows = linksbypage(days)
        df = concat([dfold, newrows])
        df.to_csv(filename)


def make_links(filename):
    startdate = '01/01/2017'
    startdate = datetime.strptime(startdate, '%d/%m/%Y')
    today = date.today()
    days1 = list(date_range(startdate, today, freq='d'))
    df = linksbypage(days1)
    df.to_csv(filename)

# make_links('LinksDOE.csv')
