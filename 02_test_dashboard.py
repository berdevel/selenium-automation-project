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

def test_dashboard_widgets_visibility(driver, request):
    # explicit wait
    wait = WebDriverWait(driver, 10)
    
    # verify that at least one of the main widgets is visible
    widget = wait.until(EC.visibility_of_element_located((By.XPATH, "//p[text()='Time at Work']")))
    assert widget.is_displayed()

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

    allure.attach(driver.get_screenshot_as_png(), 
                  name="Evidence_Screenshot", 
                  attachment_type=AttachmentType.PNG)

def test_user_profile_dropdown(driver, request):
    wait = WebDriverWait(driver, 10)
    
    # locate the username in the header
    user_dropdown = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "oxd-userdropdown-name")))
    assert user_dropdown.text != "" # Verifica que no esté vacío
    
    # click to see if the menu expands
    user_dropdown.click()
    logout_option = driver.find_element(By.LINK_TEXT, "Logout")
    assert logout_option.is_displayed()

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

    allure.attach(driver.get_screenshot_as_png(), 
                  name="Evidence_Screenshot", 
                  attachment_type=AttachmentType.PNG)

def test_sidebar_menu_count(driver, request):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "oxd-main-menu")))
    
    # get all menu items
    menu_items = driver.find_elements(By.CLASS_NAME, "oxd-main-menu-item")
    
    # orangehrm usually has 12 sections for the admin
    print(f"Secciones encontradas: {len(menu_items)}")
    assert len(menu_items) >= 10

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

    allure.attach(driver.get_screenshot_as_png(), 
                  name="Evidence_Screenshot", 
                  attachment_type=AttachmentType.PNG)