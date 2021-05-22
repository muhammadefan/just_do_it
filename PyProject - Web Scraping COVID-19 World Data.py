"""
############### COVID-19 Data Scraping ###############
selenium docs:
https://selenium-python.readthedocs.io/locating-elements.html

downloads:
- google chrome webdriver: https://chromedriver.chromium.org/downloads
- python: https://www.python.org/downloads/release/python-379/
- sublime text: https://www.sublimetext.com/3
- install some libraries through CMD (Windows) & Terminal (MacOS): pip install library_name  
"""

# importing some libraries
from selenium import webdriver # lauch google chrome
from selenium.webdriver.common.keys import Keys
import pandas as pd # playing with data


## STEP 1
# specify the path to the chromedriver.exe
driver = webdriver.Chrome('chromedriver.exe')
# accessing google.com
driver.get('https://www.google.com/')


## STEP 2
# type keyword, then enter
search_data = driver.find_element_by_name('q')
search_data.send_keys('worldometer coronavirus')
search_data.send_keys(Keys.ENTER)
# accessing first appeared article in google search
driver.find_element_by_css_selector('div.yuRUbf>a').click() #div & a=tag; yuRUbf=attribute class


## STEP 3
# number of country, max 219
country_num = 2

# collecting country's url
country_urls = driver.find_elements_by_css_selector('a.mt_a') #div=tag; mt_a=attribute class
urls_con=[]
for url in country_urls:
	urls_con.append(url.get_attribute('href'))
	if len(urls_con) == country_num:
		break
# duplicated data checking
df = pd.Series(urls_con)
if df.duplicated().sum() == 0:
	print('none duplicated data')
else:
	print('duplicated data detected')

# collecting country name
country_con=[] # for storing the data (country name)
for country in country_urls:
	country_con.append(country.text)
	if len(country_con) == country_num:
		break
# duplicated data checking
df = pd.Series(country_con)
if df.duplicated().sum() == 0:
	print('none duplicated data')
else:
	print('duplicated data detected')


## STEP 4
# accessing country's url
cases_con=[]
death_con=[]
recovered_con=[]
for url in urls_con:
	driver.get(url)

	## STEP 5
	# scrape the data
	cases = driver.find_element_by_xpath('//div[@id="maincounter-wrap"][1]//div[@class="maincounter-number"]/span')
	death = driver.find_element_by_xpath('//div[@id="maincounter-wrap"][2]//div[@class="maincounter-number"]/span')
	recovered = driver.find_element_by_xpath('//div[@id="maincounter-wrap"][3]//div[@class="maincounter-number"]/span')

	# store the data
	cases_con.append(cases.text)
	death_con.append(death.text)
	recovered_con.append(recovered.text)


## STEP 6
# store scraped data into dataframe and print it
df = pd.DataFrame({'country_name':country_con, 'total_cases':cases_con, 'total_death':death_con, 'total_recovered':recovered_con})
print(df)
# save data into csv file
df.to_csv('covid-19 data.csv') # xlsx=excel


# end the process
driver.quit()
