#!/usr/bin/python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException, NoSuchWindowException, UnexpectedAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import logging, code, time, csv, traceback, sys

logging.basicConfig(filename="script.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger()

sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.INFO)
logger.addHandler(sh)

options = Options()
options.add_argument("-profile")
options.add_argument("./firefox_selenium_profile/")

browser = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
browser.get("https://www.google.com/maps/")

# wait for manual login AOK --------------------------------------------
# input("Press RETURN key after manual login")

# iterating over places in places.csv
with open('places.csv', newline='') as csvfile:
    places = list(csv.reader(csvfile, delimiter=',', quotechar='|'))
    index = 0
    trial = 1
    while index < len(places) and (row := places[index]):
        # print(row)
        try:
    # bowser opened. opened maps --------------------------------------------
            browser.get("https://www.google.com/maps/")

            if row[0].lower() == "name": 
                index += 1
                continue
            # logging.info(f"Registering {row}")

    # retrive search box --------------------------------------------
            # need to wait untill fully loaded --------------------------------------------
            search_box = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@id='searchboxinput']")))

    # clear the search box --------------------------------------------        
            search_box.clear()

    # enter coordinates --------------------------------------------
            search_box.send_keys(','.join(row[1:]))
            search_box.send_keys(Keys.RETURN)

            
    # wait for sidebar --------------------------------------------
            add_place = WebDriverWait(browser, 6).until(EC.presence_of_element_located((By.XPATH, "//div/span/span[text()='Add a missing place']")))

    # get address for later --------------------------------------------
            address_box = browser.find_element(By.XPATH, "//button[@data-tooltip='Copy plus code']/../..").find_elements(by=By.TAG_NAME, value='span')[3]
            address = row[3] if (len(row) == 4) else address_box.text

    # open place adding dialog box --------------------------------------------
            add_place.click()

    # select into iframe that place form is loaded on --------------------------------------------
            # manual wait --------------------------------------------
            time.sleep(6)

            # switch to 2nd iframe --------------------------------------------
            place_form_iframe = browser.find_elements(by=By.TAG_NAME, value='iframe')[2]
            browser.switch_to.frame(place_form_iframe)    
            
    # input place_name --------------------------------------------
            place_name = WebDriverWait(browser, 6).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Add place name']")))
            place_name.clear()
            place_name.send_keys(f"{row[0].strip()} ATM")
            
    # select place category --------------------------------------------
            category = browser.find_element(By.XPATH, "//div[text()='Category (required)*']")
            category.click()

            # manual wait --------------------------------------------
            time.sleep(6)    
        
            # refresh iframes --------------------------------------------
            browser.switch_to.default_content()
            category_search_iframe = browser.find_elements(by=By.TAG_NAME, value='iframe')[2]
            browser.switch_to.frame(category_search_iframe)

    # select place category --------------------------------------------
            category_search_input = browser.find_element(By.XPATH, "//span[text()='Search more categories']/../../../input")
            category_search_input.send_keys("ATM")
            category_search_input.send_keys(Keys.RETURN)

            # wait for category search --------------------------------------------
            WebDriverWait(browser, 6).until(EC.element_to_be_clickable((By.XPATH, "//li/div/div[text()='ATM']"))).click()
            
    # enter required address -------------------------------------------
            time.sleep(2)
            # refresh iframes --------------------------------------------
            browser.switch_to.default_content()
            category_search_iframe = browser.find_elements(by=By.TAG_NAME, value='iframe')[2]
            browser.switch_to.frame(category_search_iframe)

            # wait for from to return --------------------------------------------
            address_input = WebDriverWait(browser, 6).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Address (required)']/../../../input")))
            
            address_input.click()
            address_input.send_keys(f"{address}, Ethiopia")
            address_input.send_keys(Keys.ESCAPE)
            address_input.send_keys(Keys.ESCAPE)
            address_input.send_keys(Keys.TAB)

    # submit form --------------------------------------------
            WebDriverWait(browser, 6).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Submit']"))).click()
            
    # move out of place_form_iframe --------------------------------------------
            browser.switch_to.default_content()
            WebDriverWait(browser, 6).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Done']"))).send_keys(Keys.ESCAPE)

            # input("Press RETURN to continue to register another place")
            logging.info(f"Successfully Registered {row}, {index}/{len(places)} -> trial {trial}")
            index += 1
            trial = 1
        except Exception as e:
            # code.interact(local=locals())
            # input("Press RETURN to repeat the same place due to error")
            if trial <= 30:
                logging.error(f"error registering {row}, {index}/{len(places)} -> trial {trial}")
                logging.debug(f"{e}")
                logging.debug(traceback.format_exc())
                trial += 1
            else:
                logging.critical(f"Skipped registering {row}, {index}/{len(places)} -> trial {trial}")
                index += 1
                trial = 1
            continue

browser.close()