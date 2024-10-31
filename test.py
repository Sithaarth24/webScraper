from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re as re


if __name__ == '__main__':
    _input = "moto g84 5g"
    _input = re.sub(r'\s+', '+' , _input)

    URL = 'https://www.flipkart.com/search?q=' + _input

    # Initialize Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (without opening the browser window)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')


    # Replace the executable path with the path to your chromedriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Visit the URL
    driver.get(URL)

    # Get page content
    page_content = driver.page_source

    print(page_content)  # Optional: to check the loaded HTML

    # Close the browser
    driver.quit()
