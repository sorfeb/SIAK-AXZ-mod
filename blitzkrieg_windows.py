import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import time
import undetected_chromedriver as uc
from fake_useragent import UserAgent

def human_delay(min_delay=1, max_delay=5, function_name="Unknown Function"):
    """Adds a random delay to simulate human-like behavior and logs the delay."""
    delay = random.uniform(min_delay, max_delay)
    print(f"[{function_name}] Human delay: {delay:.2f} seconds")
    time.sleep(delay)

def war(driver, username, password):
    """Main function to perform the war process."""
    print("[war] Starting war function")
    matkul = load_matkul("matkul.txt")
    siak_url = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanEdit"

    try:
        login(driver, username, password)
        
        while not check_page(driver, siak_url, "Pesan untuk pembimbing akademis"):
            logout(driver)
            login(driver, username, password)
        
        while True:
            if select_courses(driver, matkul):
                break
            driver.get(siak_url)
        
        print("[war] War completed successfully")
    except Exception as e:
        print(f"[war] An error occurred: {e}")
    finally:
        print("[war] Closing the browser.")
        driver.quit()

def load_matkul(filename):
    """Load matkul from a file into a list."""
    print("[load_matkul] Loading matkul from file")
    with open(filename) as file_inp:
        return [line.strip() for line in file_inp]

def check_page(driver, url, expected_text):
    """Check if a specific text exists on a page."""
    print(f"[check_page] Checking page: {url}")
    try:
        driver.get(url)
        human_delay(8, 12, "check_page")
        return expected_text in driver.page_source
    except WebDriverException as e:
        print(f"[check_page] Error: {e}")
        return False

def select_courses(driver, matkul):
    """Try selecting courses and submitting the IRS form."""
    print("[select_courses] Attempting to select courses")
    try:
        for kelas in matkul:
            try:
                clicked = driver.find_element("xpath", f'//input[@value="{kelas}"]')
                ActionChains(driver).move_to_element(clicked).click().perform()
                human_delay(1, 3, "select_courses")
            except NoSuchElementException:
                print(f"[select_courses] Course {kelas} not found, skipping")
                continue

        driver.find_element("name", 'submit').click()
        human_delay(2, 5, "select_courses")

        if "IRS berhasil tersimpan!" in driver.page_source and "Daftar IRS" in driver.page_source:
            print("[select_courses] IRS successfully submitted!")
            return True
    except NoSuchElementException as e:
        print(f"[select_courses] Element not found: {e}")
    return False

def login(driver, username, password):
    """Log in to the SIAK website."""
    print(f"[login] Logging in with username: {username}")
    while True:
        try:
            driver.get("https://academic.ui.ac.id/main/Authentication/")
            driver.find_element("id", "u").send_keys(username)
            driver.find_element("name", "p").send_keys(password, Keys.RETURN)
            human_delay(2, 5, "login")

            if "Logout Counter" in driver.page_source:
                print("[login] Login successful")
                break
        except WebDriverException as e:
            print(f"[login] Login failed: {e}")
            continue

def logout(driver):
    """Log out from the SIAK website."""
    print("[logout] Logging out")
    while True:
        try:
            driver.get("https://academic.ui.ac.id/main/Welcome/Index")
            driver.find_element("partial link text", 'Logout').click()
            human_delay(2, 4, "logout")
            if driver.find_element("id", "u"):
                print("[logout] Logout successful")
                break
        except WebDriverException as e:
            print(f"[logout] Logout failed: {e}")
            continue

if __name__ == "__main__":
    uspass = []
    try:
        with open('credentials.txt') as file_inp:
            for line in file_inp:
                uspass.append(line.strip())

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
        options.add_argument("--disable-blink-features=AutomationControlled")  
        options.add_argument("--incognito") 
        options.add_argument("--disable-plugins-discovery")  
        options.add_argument("--disable-infobars") 


        driver = uc.Chrome(options=options)

        war(driver, uspass[0], uspass[1])

    except KeyboardInterrupt:
        print("\n[main] Script interrupted by user. Exiting gracefully...")
    except Exception as e:
        print(f"[main] Unexpected error: {e}")
    finally:
        try:
            driver.quit()
        except NameError:
            print("[main] Driver was not initialized. Exiting...")
