import datetime
import os
import sys

from selenium import webdriver


def extract_num(s: str):
    r = ""
    for c in s:
        if c.isdigit():
            r += c
    return r


def get_inns(driver, url):
    driver.get(url)
    good = []
    bad = []
    try:
        text = driver.find_element_by_xpath("//b[text()='Должник']/../following-sibling::table[1]/descendant::td[contains(text(),'ИНН')]/following-sibling::td").text.strip()
        if len(text) == 10:
            good.append(text)
        # else a person
    except Exception as e:
        for el in driver.find_elements_by_xpath("//*[contains(text(),'ИНН')]"):
            for seq in el.text.strip().split(','):
                if seq.count('ИНН') > 0:
                    inn = extract_num(seq)
                    if len(inn) == 10:
                        bad.append(inn)
    return good, bad


chrome_options = webdriver.chrome.options.Options()
chrome_options.headless = True
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(1)

YEAR = int(os.getenv("YEAR", 2013))
YEAR_END = int(os.getenv("YEAR_END", 2014))
print(YEAR, YEAR_END)
sys.stdout.flush()
d = datetime.datetime(YEAR, 1, 1)

fgood = open(f'{YEAR}_good.txt', 'a')
fbad = open(f'{YEAR}_bad.txt', 'a')
while d < datetime.datetime(YEAR_END, 1, 1):
    ds = d.strftime("%d.%m.%Y")
    ds2 = d.strftime("%Y.%m.%d")
    good = []
    bad = []
    with open('out/' + ds + '.txt', 'r') as f:
        for line in f.readlines():
            g, b = get_inns(driver, line)
            for item in g:
                good.append((ds2, item))
            for item in b:
                bad.append((ds2, item))
    for item in good:
        fgood.write('\t'.join(item) + '\n')
    for item in bad:
        fbad.write('\t'.join(item) + '\n')
    d += datetime.timedelta(days=1)
    # sleep(1)
fgood.close()
fbad.close()
