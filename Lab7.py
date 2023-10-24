import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

url = 'https://www.audible.com/adblbestsellers?ref_pageloadid=h7Ag5cGcQ5yvRAVu&ref=a_search_b1_desktop_footer_column_2_0&pf_rd_p=6a55a63d-48d3-4d5e-857f-ae6682380e4d&pf_rd_r=65QXM553SAAQNRH2VDV2&pageLoadId=yGFSdjIrgVpQDcAP&ref_plink=not_applicable&creativeId=2d835e86-1f10-4f6e-a4c6-33d2001684e6'

driver = webdriver.Chrome(service = ChromeService(ChromeDriverManager().install()))
driver.get(url)

titles = []
authors = []
runtimes = []
release_dates = []
list_numbers = []

for i in range(5):
    container = driver.find_element(By.CLASS_NAME, 'adbl-impression-container')
    products = container.find_elements(By.XPATH, './/li[contains(@class, "productListItem")]')

    for product in products:
        book = product.find_element(By.XPATH, './/h3[contains(@class, "bc-heading")]').text.split('. ')
        list_numbers.append(book[0])
        titles.append(book[1])

    for product in products:
        name = product.find_element(By.XPATH, './/li[contains(@class, "authorLabel")]').text
        authors.append(name[4:])

    for product in products:
        rtime = product.find_element(By.XPATH, './/li[contains(@class, "runtimeLabel")]').text
        runtimes.append(rtime[8:])

    for product in products:
        date = product.find_element(By.XPATH, './/li[contains(@class, "releaseDateLabel")]').text
        release_dates.append(date[14:])

    driver.find_element(By.XPATH, './/span[contains(@class, "nextButton")]').click()



bestsellers = pd.DataFrame({"title" : titles, "author" : authors, "runtime" : runtimes, "release_date" : release_dates, "list_number" : list_numbers})

bestsellers.to_csv('./audiobooks.csv', index=False)

driver.quit()