from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

# Set the path to the ChromeDriver executable
chrome_driver_path = r"C:\Users\srika\Downloads\chromedriver-win32\chromedriver-win32\chromedriver.exe"

# Create a ChromeOptions object
chrome_options = ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--allow-running-insecure-content')
chrome_options.add_argument('--disable-web-security')


# Create a ChromeService object
chrome_service = ChromeService(executable_path=chrome_driver_path)

# Create a Chrome WebDriver instance with the ChromeService and ChromeOptions
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Open YouTube website
driver.get("https://www.youtube.com")

# Function to close newly opened tabs
def close_new_tabs():
    original_tab = driver.window_handles[0]
    for tab in driver.window_handles[1:]:
        driver.switch_to.window(tab)
        driver.close()
    driver.switch_to.window(original_tab)

# Example: Open a new tab (you can modify this as needed)
driver.execute_script("window.open('about:blank', '_blank');")

# Close the new tab(s)
while True:
    close_new_tabs()
