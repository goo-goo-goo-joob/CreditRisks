import datetime
from time import sleep

from selenium import webdriver
from selenium.webdriver.support.ui import Select


def clr_table(driver):
    try:
        driver.execute_script("return document.getElementById('{}').remove();".format(
            driver.find_element_by_xpath("//th[text()='Тип сообщения']/ancestor::table[1]").get_property('id')
        ))
    except Exception:
        pass


chrome_options = webdriver.chrome.options.Options()
chrome_options.headless = True
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(3)
driver.get('https://bankrot.fedresurs.ru/Messages.aspx')

driver.find_element_by_id('ctl00_cphBody_mdsMessageType_tbSelectedText').click()

iframe = driver.find_element_by_xpath("//form//iframe")
driver.switch_to.frame(iframe)
for i in range(1000):
    try:
        driver.find_element_by_xpath("//span[text()='Сообщение о судебном акте']").click()
        break
    except Exception:
        sleep(0.01)
driver.switch_to.default_content()

for i in range(1000):
    try:
        Select(driver.find_element_by_id('ctl00_cphBody_ddlCourtDecisionType')).select_by_visible_text("о признании должника банкротом и открытии конкурсного производства")
        break
    except Exception:
        sleep(0.01)

d = datetime.datetime(2012, 1, 1)

clr_table(driver)
while d < datetime.datetime(2018, 1, 1):

    ds = d.strftime("%d.%m.%Y")

    input_begin = driver.find_element_by_id('ctl00_cphBody_cldrBeginDate_tbSelectedDate')

    input_begin.clear()
    input_begin.send_keys(ds)

    input_end = driver.find_element_by_id('ctl00_cphBody_cldrEndDate_tbSelectedDate')
    input_end.clear()
    input_end.send_keys(ds)

    driver.find_element_by_id("ctl00_cphBody_ibMessagesSearch").click()

    result = []
    PAGE_SIZE = 50
    page = 0
    while page * PAGE_SIZE == len(result):
        for el in driver.find_elements_by_xpath("//a[contains(text(),'Сообщение о судебном акте')]"):
            result.append(el.get_property("href"))
        page += 1
        if page * PAGE_SIZE == len(result):
            try:
                driver.find_element_by_xpath("""//a[@href="javascript:__doPostBack('ctl00$cphBody$gvMessages','Page${}')"]""".format(page + 1)).click()
                clr_table(driver)
            except Exception:
                break
        else:
            break
    clr_table(driver)
    with open("out/" + ds + ".txt", 'w', encoding='utf8') as f:
        f.write('\n'.join(result))
    print(ds, len(result))

    d += datetime.timedelta(days=1)
    sleep(1)
pass
