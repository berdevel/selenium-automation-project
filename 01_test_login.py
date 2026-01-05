import pytest
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    
    yield driver
    
    driver.quit()

def test_login_to_orangehrm(driver, request):
    """
    login test
    """
    # 1. test actions
    driver.find_element(by=By.NAME, value="username").send_keys("Admin")
    driver.find_element(by=By.NAME, value="password").send_keys("admin123")
    driver.find_element(by=By.CSS_SELECTOR, value="button").click()


    # 2. explicit wait: wait until the element becomes visible
    wait = WebDriverWait(driver, 10)
    dashboard_element = wait.until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, "oxd-sidepanel"))
    )

    # 3. first assertions
    expected_url = "https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index"
    expected_title = "OrangeHRM"

    # 4. get screenshots
    # make dir 'screenshots' if not exist
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    # get test name
    test_name = request.node.name
    timestamp = datetime.now().strftime("%H-%M-%S")
    
    # save screenshot
    file_path = f"screenshots/{test_name}_{timestamp}.png"
    driver.save_screenshot(file_path)
    print(f"\nCaptura guardada en: {file_path}")

    # execute finally asserts
    assert driver.current_url == expected_url
    assert driver.title == expected_title