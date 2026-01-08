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

def test_logout_orangehrm(driver, request):
    wait = WebDriverWait(driver, 10)

    # 1. click on the username (top right corner)
    # this opens the hidden menu
    user_dropdown = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "oxd-userdropdown-name")))
    user_dropdown.click()

    # 2. wait for the 'logout' option to become visible and click it.
    # we use LINK_TEXT because it's an <a> tag with the exact text.
    logout_link = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Logout")))
    logout_link.click()

    # 3. verify that we've returned to the login page
    # a reliable way to do this is to check that the username field is present again.
    wait.until(EC.presence_of_element_located((By.NAME, "username")))
    
    current_url = driver.current_url
    assert "login" in current_url
    print(f"Logout exitoso en {request.node.name}. URL actual: {current_url}")

    # take a screenshot of the post-logout login page
    import os
    if not os.path.exists("screenshots"): os.makedirs("screenshots")
    driver.save_screenshot(f"screenshots/logout_success_{request.node.name}.png")

    allure.attach(driver.get_screenshot_as_png(), 
                  name="Evidence_Screenshot", 
                  attachment_type=AttachmentType.PNG)