from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def get_lvl(driver, login):
    profile_url = f"{base_url}{login}"
    driver.get(profile_url)
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.progress-container[data-cursus="42cursus"]'))
        )
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        element = soup.select_one('a.progress-container[data-cursus="42cursus"]')
        if element:
            text = element.select_one('div.on-progress').text.strip()
            level = text.split()[1]
            percentage = text.split()[3][:-1]
            exp = float(level) + float(percentage) / 100.0
            return exp
        else:
            print(f"No se encontró el elemento progress-container para {login}")
            return None
    except Exception as e:
        print(f"No se pudo obtener la información para {login}: {e}")
        return None

user_logins = []

with open('/home/imontero/42/Ft_Trascendence/backend/api/user_logins.txt', 'r') as file:
    for login in file:
        login = login.strip()
        user_logins.append(login)



firefox_profile_path = '/home/imontero/.mozilla/firefox/d7jmh8qi.default-release'
options = webdriver.FirefoxOptions()
options.set_preference("browser.link.open_newwindow.restriction", 0)
options.set_preference("browser.link.open_newwindow", 1)
options.set_preference("browser.link.open_newwindow.override.external", 2)
options.set_preference("browser.link.open_newwindow.restriction", 0)
options.profile = firefox_profile_path 

service = webdriver.FirefoxService(executable_path="/home/imontero/42/Ft_Trascendence/backend/api/geckodriver")

driver = webdriver.Firefox(service=service, options=options)

base_url = 'https://profile.intra.42.fr/users/'

output_file = '/home/imontero/42/Ft_Trascendence/backend/api/levels.txt'
i = 0
with open(output_file, 'w') as outfile:
    for login in user_logins:
        profile_url = f"{base_url}{login}"
        time.sleep(0.5) 

        driver.get(profile_url)
        level = get_lvl(driver, login)

        if level is not None:
            outfile.write(f"Login: {login}, Nivel: {level}\n")
            print(f"{i}, Login: {login}, Nivel: {level}")
            i += 1
        else:
            outfile.write(f"Login: {login}, Nivel: None\n")
            print(f"Login: {login}, Nivel: None")

driver.quit()
