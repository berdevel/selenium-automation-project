import pytest
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
from allure_commons.types import AttachmentType

@pytest.fixture(params=["chrome", "firefox", "edge"])
def driver(request):
    """
    fixture to config webdriver and manage clean
    """
    browser = request.param
    if browser == "chrome":
        driver = webdriver.Chrome()
    elif browser == "firefox":
        driver = webdriver.Firefox()
    elif browser == "edge":
        driver = webdriver.Edge()
    
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    driver.maximize_window()
    driver.implicitly_wait(10)

    driver.find_element(by=By.NAME, value="username").send_keys("Admin")
    driver.find_element(by=By.NAME, value="password").send_keys("admin123")
    driver.find_element(by=By.CSS_SELECTOR, value="button").click()

    wait = WebDriverWait(driver, 10)
    dashboard_element = wait.until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, "oxd-sidepanel"))
    )
    
    yield driver
    
    driver.quit()

def test_directory_search_by_job_title(driver, request):
    wait = WebDriverWait(driver, 10)

    # 1. navigate to the 'directory' menu
    # look for the link containing the text 'directory' in the sidebar menu
    directory_menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Directory']")))
    directory_menu.click()

    # 2. interacting with the 'job title' filter
    # in orangehrm, dropdowns are custom, not standard <select> elements
    job_title_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='oxd-select-text-input'])[1]")))
    job_title_dropdown.click()

    # we select an option (e.g., 'account assistant')
    option = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='listbox']//span[text()='Account Assistant']")))
    option.click()

    # 3. click on the 'search' button
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # 4. validate that results or a loading message are displayed
    # we wait for the employee card container to appear
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "orangehrm-directory-card")))
    
    results = driver.find_elements(By.CLASS_NAME, "orangehrm-directory-card")
    print(f"Empleados encontrados con ese cargo: {len(results)}")
    
    # screenshot of the result
    if not os.path.exists("screenshots"): os.makedirs("screenshots")
    driver.save_screenshot(f"screenshots/directory_search_{request.node.name}.png")

    allure.attach(driver.get_screenshot_as_png(), 
                  name="Evidence_Screenshot", 
                  attachment_type=AttachmentType.PNG)

    assert len(results) > 0, "No se encontraron empleados para el cargo seleccionado"