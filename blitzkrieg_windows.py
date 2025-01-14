import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import undetected_chromedriver as uc
from fake_useragent import UserAgent

def human_delay(min_delay=1, max_delay=5):
    """Adds a random delay to simulate human-like behavior."""
    time.sleep(random.uniform(min_delay, max_delay))

def war(username, password):
    """Main function to perform the war process."""
    user_agent = UserAgent().random  # Random user agent for better anonymity

    options = uc.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--disable-extensions')
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')

    driver = uc.Chrome(options=options)
    driver.set_page_load_timeout(100)

    login(driver, username, password)

    matkul = load_matkul("matkul.txt")
    siak_url = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanEdit"

    while not check_page(driver, siak_url, "Pesan untuk pembimbing akademis"):
        logout(driver)
        login(driver, username, password)

    while True:
        if select_courses(driver, matkul):
            break
        driver.get(siak_url)

    print("Heil")
    input()
    driver.close()

def load_matkul(filename):
    """Load matkul from a file into a list."""
    with open(filename) as file_inp:
        return [line.strip() for line in file_inp]

def check_page(driver, url, expected_text):
    """Check if a specific text exists on a page."""
    try:
        driver.get(url)
        human_delay(8, 12)
        return expected_text in driver.page_source
    except:
        return False

def select_courses(driver, matkul):
    """Try selecting courses and submitting the IRS form."""
    try:
        for kelas in matkul:
            try:
                clicked = driver.find_element("xpath", f'//input[@value="{kelas}"]')
                ActionChains(driver).move_to_element(clicked).click().perform()
                human_delay(1, 3)
            except NoSuchElementException:
                continue

        driver.find_element("name", 'submit').click()
        human_delay(2, 5)

        if "IRS berhasil tersimpan!" in driver.page_source and "Daftar IRS" in driver.page_source:
            return True

    except NoSuchElementException:
        pass
    return False

def login(driver, username, password):
    """Log in to the SIAK website."""
    while True:
        try:
            driver.get("https://academic.ui.ac.id/main/Authentication/")
            driver.find_element("id", "u").send_keys(username)
            driver.find_element("name", "p").send_keys(password, Keys.RETURN)
            human_delay(2, 5)

            if "Logout Counter" in driver.page_source:
                break
        except:
            continue

def logout(driver):
    """Log out from the SIAK website."""
    while True:
        try:
            driver.get("https://academic.ui.ac.id/main/Welcome/Index")
            driver.find_element("partial link text", 'Logout').click()
            human_delay(2, 4)
            if driver.find_element("id", "u"):
                break
        except:
            continue

if __name__ == "__main__":
    uspass = []
    with open('credentials.txt') as file_inp:
        for line in file_inp:
            uspass.append(line.strip())

    war(uspass[0], uspass[1])
