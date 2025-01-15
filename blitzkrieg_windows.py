import random
import time
import pyautogui
from colorama import Fore, Style, init

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By  

import undetected_chromedriver as uc
from fake_useragent import UserAgent

# Initialize colorama for colored output
init(autoreset=True)

# Define distinct colors for each tag
COLORS = {
    "war": Fore.RED,
    "login": Fore.GREEN,
    "logout": Fore.CYAN,
    "load_matkul": Fore.MAGENTA,
    "check_page": Fore.YELLOW,
    "select_courses": Fore.BLUE,
    "human_delay": Fore.WHITE,
    "error": Fore.LIGHTRED_EX
}

def color_tag(tag, message):
    """Format message with color for the given tag."""
    return f"{COLORS.get(tag, Fore.WHITE)}[{tag}] {message}"

def human_delay(min_delay=1, max_delay=5, function_name="Unknown Function"):
    """Adds a random delay to simulate human-like behavior and logs the delay."""
    delay = random.uniform(min_delay, max_delay)
    print(color_tag("human_delay", f"{function_name} - Human delay: {delay:.2f} seconds"))
    time.sleep(delay)

def simulate_mouse_movement():
    """Simulates human-like mouse movement."""
    x, y = random.randint(100, 500), random.randint(100, 500)
    print(color_tag("human_delay", f"Moving mouse to: ({x}, {y})"))
    pyautogui.moveTo(x, y, duration=random.uniform(0.5, 1.5))

def war(driver, username, password):
    """Main function to perform the war process."""
    print(color_tag("war", "Starting war function"))
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
        
        print(color_tag("war", "War completed successfully"))
    except Exception as e:
        print(color_tag("error", f"An error occurred: {e}"))
    finally:
        print(color_tag("war", "Closing the browser."))
        driver.quit()

def load_matkul(filename):
    """Load matkul from a file into a list."""
    print(color_tag("load_matkul", "Loading matkul from file"))
    with open(filename) as file_inp:
        return [line.strip() for line in file_inp]

def check_page(driver, url, expected_text):
    """Check if a specific text exists on a page."""
    print(color_tag("check_page", f"Checking page: {url}"))
    try:
        driver.get(url)
        human_delay(5, 10, "check_page")
        return expected_text in driver.page_source
    except WebDriverException as e:
        print(color_tag("error", f"Error: {e}"))
        return False

def select_courses(driver, matkul):
    """Try selecting courses and submitting the IRS form."""
    print(color_tag("select_courses", "Attempting to select courses"))
    try:
        for kelas in matkul:
            try:
                element  = driver.find_element("xpath", f'//input[@value="{kelas}"]')
                simulate_mouse_movement()
                driver.execute_script("arguments[0].scrollIntoView();", element)
                driver.execute_script("arguments[0].click();", element)
                human_delay(1, 3, "select_courses")
            except NoSuchElementException:
                print(color_tag("select_courses", f"Course {kelas} not found, skipping"))
                continue

        submit_button = driver.find_element(By.NAME, 'submit')
        simulate_mouse_movement()
        driver.execute_script("arguments[0].click();", submit_button)
        human_delay(0.1, 0.3, "select_courses")

        if "IRS berhasil tersimpan!" in driver.page_source and "Daftar IRS" in driver.page_source:
            print(color_tag("select_courses", "IRS successfully submitted!"))
            return True
    except NoSuchElementException as e:
        print(color_tag("error", f"Element not found: {e}"))
    return False

def login(driver, username, password):
    """Log in to the SIAK website."""
    print(color_tag("login", f"Logging in with username: {username}"))
    while True:
        try:
            driver.get("https://academic.ui.ac.id/main/Authentication/")
            driver.find_element("id", "u").send_keys(username)
            driver.find_element("name", "p").send_keys(password, Keys.RETURN)
            human_delay(2, 5, "login")

            if "Logout Counter" in driver.page_source:
                print(color_tag("login", "Login successful"))
                break
        except WebDriverException as e:
            print(color_tag("error", f"Login failed: {e}"))
            continue

def logout(driver):
    """Log out from the SIAK website."""
    print(color_tag("logout", "Logging out"))
    while True:
        try:
            driver.get("https://academic.ui.ac.id/main/Welcome/Index")
            logout_button = driver.find_element(By.PARTIAL_LINK_TEXT, 'Logout')
            simulate_mouse_movement()
            driver.execute_script("arguments[0].click();", logout_button)
            human_delay(2, 4, "logout")
            if driver.find_element(By.ID, "u"):
                print(color_tag("logout", "Logout successful"))
                break
        except WebDriverException as e:
            print(color_tag("error", f"Logout failed: {e}"))
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
        print(color_tag("error", "\n[main] Script interrupted by user. Exiting gracefully..."))
    except Exception as e:
        print(color_tag("error", f"[main] Unexpected error: {e}"))
    finally:
        try:
            driver.quit()
        except NameError:
            print(color_tag("error", "[main] Driver was not initialized. Exiting..."))
