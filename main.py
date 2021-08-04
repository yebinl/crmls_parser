# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import time
import csv
import datetime

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

################################################################################

# Firefox webdriver settings

fp = webdriver.FirefoxProfile()

# # disable images and styles
# fp.set_preference('permissions.default.stylesheet', 2)
# fp.set_preference('permissions.default.image', 2)
# fp.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

fp.update_preferences()
options = Options()
options.headless = False

##################################################################################

# initial firefox webdriver
driver = webdriver.Firefox(options=options, firefox_profile=fp)
# initial listing urls
listing_urls = []

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

# close popup window
def close_popup(popup_id: str = "0") -> None:
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f"#{popup_id}")))  # seconds
        driver.find_element_by_id(popup_id).click()
        print("Closing popup...")
    except:
        pass

def close_user_conflict():
    try:
        current_url_link = driver.current_url
        if "LoginIntermediate" in current_url_link:
            continue_btn = driver.find_elements_by_id("btnContinue")
            if len(continue_btn) < 1:
                print("User conflict but cannot locate continue button...")
                return
            driver.execute_script("arguments[0].click();", continue_btn[0])
            wait = WebDriverWait(driver, 15)
            wait.until(EC.url_changes(current_url_link))
    except:
        pass

# login crmls site
def login(user: str, pswd: str):
    login_url = "https://login.cl.crmls.org/idp/login/"
    driver.get(login_url)

    # wait sec should >10, at least on Linux
    wait = WebDriverWait(driver, 15)

    # handle security check
    if "LoginRedirect" in driver.current_url:
        login_button = driver.find_elements_by_class_name('button_redirect1')
        if len(login_button) < 1:
            print("Cannot pass security check...")
            return False
        driver.execute_script("arguments[0].click();", login_button[0])
        time.sleep(10)


    if "login" in driver.current_url:
        wait.until(EC.presence_of_element_located((By.ID, "clareity")))
        login_input = driver.find_elements_by_id("clareity")
        if len(login_input) < 1:
            print("Cannot find login input...")
            return False
        # login
        login_input[0].send_keys(user, Keys.TAB, pswd, Keys.ENTER)
        wait.until(EC.url_changes(login_url))
        time.sleep(10)

    if "dashboard" in driver.current_url:
        print("Logged in")
        return True
    else:
        print("Failed to login...")
        return False

# Crawl result listings
def get_listing_urls(city: str, bedrooms: str):
    search_url = "https://matrix.crmls.org/Matrix/Search/ResidentialLease/Detail"
    driver.get(search_url)
    time.sleep(10)

    # handle another user check box
    close_user_conflict()
    time.sleep(5)

    # locate input boxes
    coming_soon_check_box = driver.find_elements_by_xpath("//input[@data-mtx-track='Status - Coming Soon']")
    active_check_box = driver.find_elements_by_xpath("//input[@data-mtx-track='Status - Active']")
    city_input_box = driver.find_elements_by_xpath("//input[@data-mtx-track='City - Textbox']")
    bedrooms_input_box = driver.find_elements_by_xpath("//input[@data-mtx-track='Bedrooms']")
    if len(coming_soon_check_box) < 1:
        print("Cannot locate coming soon check box...")
        return
    if len(active_check_box) < 1:
        print("Cannot locate active check box...")
        return
    if len(city_input_box) < 1:
        print("Cannot locate city text input box...")
        return
    if len(bedrooms_input_box) < 1:
        print("Cannot locate city text input box...")
        return

    # inject filter inputs
    driver.execute_script("arguments[0].click();", coming_soon_check_box[0]) # click coming soon
    driver.execute_script("arguments[0].click();", active_check_box[0])  # click active
    city_input_box[0].send_keys(city) # enter city input
    if bedrooms != "":
        bedrooms_input_box[0].send_keys(bedrooms) # enter bedrooms filter
    time.sleep(5)

# Crawl result listings
def get_listing_urls2(city: str, distance: str, bedrooms: str):
    search_url = "https://matrix.crmls.org/Matrix/Search/ResidentialLease/Detail"
    driver.get(search_url)
    time.sleep(10)

    # handle another user check box
    close_user_conflict()
    time.sleep(5)

    # locate input boxes
    coming_soon_check_box = driver.find_elements_by_xpath("//input[@data-mtx-track='Status - Coming Soon']")
    active_check_box = driver.find_elements_by_xpath("//input[@data-mtx-track='Status - Active']")
    city_input_box = driver.find_elements_by_id("Fm21_Ctrl12_TB")
    distance_input_box = driver.find_elements_by_class_name("mapSearchDistance")
    bedrooms_input_box = driver.find_elements_by_xpath("//input[@data-mtx-track='Bedrooms']")
    if len(coming_soon_check_box) < 1:
        print("Cannot locate coming soon check box...")
        return
    if len(active_check_box) < 1:
        print("Cannot locate active check box...")
        return
    if len(city_input_box) < 1:
        print("Cannot locate city text input box...")
        return
    if len(distance_input_box) < 1:
        print("Cannot locate distance input box...")
        return
    if len(bedrooms_input_box) < 1:
        print("Cannot locate city text input box...")
        return

    # inject filter inputs
    driver.execute_script("arguments[0].click();", coming_soon_check_box[0]) # click coming soon
    driver.execute_script("arguments[0].click();", active_check_box[0])  # click active
    time.sleep(1)
    distance_input_box[0].send_keys(Keys.BACKSPACE, Keys.BACKSPACE, distance)
    time.sleep(1)
    city_input_box[0].send_keys(city) # enter city input
    time.sleep(1)
    select_box = driver.find_elements_by_class_name("mapSearchDialog")
    if len(select_box) < 1:
        print("Cannot locate city pop up box...")
        return
    select_box[0].find_element_by_xpath(".//ul[@class='disambiguation']/li[2]").click()
    if bedrooms != "":
        bedrooms_input_box[0].send_keys(bedrooms) # enter bedrooms filter
    time.sleep(5)

def crawl_all_results(city: str):
    # view results
    result_button = driver.find_elements_by_id("m_ucResultsPageTabs_m_lbResultsTab")
    if len(result_button) < 1:
        print("Cannot locate result button...")
        return
    driver.execute_script("arguments[0].click();", result_button[0]) # see result
    time.sleep(10)

    headers = ["Area", "Address", "Crmls ID", "Price", "Bed#", "Sqft", "Status", "Available Date", "Owner's Name", "Instruction", "Agent", "Agent Cell", "Agent Direct", "Agent Email", "Office Phone", "Office", "OCRealtors URL"]
    with open(f"Output/{city}_result.csv", 'w', newline='', encoding="utf-8") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(headers)

        # crawl all urls
        while True:
            # extract all urls by actually get inside a tags
            line_items = driver.find_elements_by_id("wrapperTable")
            if len(line_items) < 1:
                print("Cannot see result items in result page...")
                return
            for index in range(0, len(line_items)):
                line_items = driver.find_elements_by_id("wrapperTable")
                listing_a_tag = line_items[index].find_elements_by_xpath(".//td[@class='d8m8']//a")
                if len(listing_a_tag) < 1:
                    print("Cannot locate a tag in result page...")
                    continue
                driver.execute_script("arguments[0].click();", listing_a_tag[0]) # click the listing link
                time.sleep(5)
                # listing_urls.append(driver.current_url)
                table = driver.find_elements_by_id("wrapperTable")
                if len(table) < 1:
                    print("Cannot locate table in result details page...")
                    driver.back()
                    time.sleep(5)
                    continue
                try:
                    address = driver.find_element_by_xpath("//*[@id='wrapperTable']/tbody/tr/td/table/tbody/tr[3]/td/table[1]/tbody/tr/td[2]/span").text
                    area = driver.find_element_by_xpath("//span[contains(text(), 'AREA:')]/following-sibling::span[2]").text
                    list_price = driver.find_element_by_xpath("//span[contains(text(), 'LIST PRICE')]/following-sibling::span[2]").text
                    bedroom_numbers = driver.find_element_by_xpath("//span[contains(text(), 'BED / BATH')]/following-sibling::span[2]").text
                    sqft_number = driver.find_element_by_xpath("//span[contains(text(), 'SQFT(src)')]/following-sibling::span[2]").text
                    active_status = driver.find_element_by_xpath("//span[contains(text(), 'STATUS')]/following-sibling::span[2]").text
                    if active_status == "Coming Soon":
                        available_date = driver.find_element_by_xpath("//span[contains(text(), 'STATUS')]/following-sibling::span[5]").text.replace(' ', '').replace('StartShowing:', '')
                    else:
                        available_date = ""
                    leasing_agent = driver.find_element_by_xpath("//span[contains(text(), 'LA:')]/following-sibling::span[4]").text
                    leasing_office = driver.find_element_by_xpath("//span[contains(text(), 'LO:')]/following-sibling::span[4]").text
                    office_phone = driver.find_element_by_xpath("//span[text()='LO PHONE:']/following-sibling::span[2]").text
                    listing_link = driver.current_url

                    try:
                        instruction_content = driver.find_element_by_xpath("//span[contains(text(), 'SHOWING INSTRUCTION')]/following-sibling::span[2]").text
                    except:
                        instruction_content = "NA"

                    try:
                        agent_cell = driver.find_element_by_xpath(
                            "//span[contains(text(), 'LA CELL')]/following-sibling::span[2]").text
                    except:
                        agent_cell = ""

                    try:
                        agent_direct = driver.find_element_by_xpath(
                            "//span[contains(text(), 'LA DIRECT')]/following-sibling::span[2]").text
                    except:
                        agent_direct = ""

                    try:
                        agent_email = driver.find_element_by_xpath(
                            "//span[contains(text(), 'LA EMAIL')]/following-sibling::span[2]").text
                    except:
                        agent_email = ""

                    try:
                        mls_listing_id = driver.find_element_by_xpath(
                            "//span[contains(text(), 'LISTING ID')]/following-sibling::span[2]").text
                    except:
                        mls_listing_id = ""

                    try:
                        parcel_link = driver.find_element_by_xpath("//span[contains(text(), 'PARCEL #:')]/following-sibling::span[2]/a")
                        try:
                            driver.get(parcel_link.get_attribute("href"))
                            time.sleep(6)
                            owner_name = driver.find_element_by_xpath("//td[contains(text(), 'Owner Name')]/following-sibling::td[1]").text
                            driver.back()
                            time.sleep(5)
                        except:
                            owner_name = ""
                            driver.back()
                            time.sleep(5)
                            pass
                    except:
                        print("Parcel link missing")
                        owner_name = ""
                        pass

                    line_content = [area, address, mls_listing_id, list_price, bedroom_numbers, sqft_number, active_status, available_date, owner_name, instruction_content, leasing_agent, agent_cell, agent_direct, agent_email, office_phone, leasing_office, listing_link]
                    csv_writer.writerow(line_content)
                except Exception as e:
                    print(str(e))
                    print("Failed to grab infos from result details page...")
                    driver.back()
                    time.sleep(5)
                    continue

                # return to the previous page
                driver.back()
                time.sleep(5)

            # check if is the end of the page
            pagination = driver.find_elements_by_id("m_upPaging")
            if len(pagination) < 1:
                print("Cannot locate pagination in result page...")
                return
            next_btn = pagination[0].find_elements_by_xpath(".//a[text()='Next']")
            if len(next_btn) < 1:
                print("Cannot locate next button in result page...")
                return
            if next_btn[0].get_attribute('disabled') == 'true':
                print("Ok! Finished all urls' crawling!")
                break
            else:
                print("Next...")
                driver.execute_script("arguments[0].click();", next_btn[0])
                time.sleep(5)



def crawl_ocrealtor(city: str, bedrooms="") -> None:
    try:
        # new session in a new window for each account because of
        # selenium.common.exceptions.StaleElementReferenceException
        driver.maximize_window()

        login_result = login("ocliuyong", "Longwise2021")
        if not login_result:
            return
        time.sleep(5)

        # get_listing_urls(city, bedrooms)
        get_listing_urls2(city, 12, bedrooms)
        crawl_all_results(city+"_"+datetime.date.today().strftime('%Y-%m-%d'))

    except Exception as e:
        print(str(e))
        print("Error")
    finally:
        driver.close()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    crawl_ocrealtor("San Jose", "3+")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
