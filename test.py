import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.fixture(params=["chrome", "firefox", "edge"])
def driver(request):
    """
    Pytest fixture to set up and tear down the WebDriver for each browser.
    """
    browser = request.param
    if browser == "chrome":
        driver = webdriver.Chrome()
    elif browser == "firefox":
        driver = webdriver.Firefox()
    elif browser == "edge":
        driver = webdriver.Edge()
    
    driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    driver.fullscreen_window()
    driver.implicitly_wait(10)
    
    yield driver
    
    driver.quit()

def test_login_to_orangehrm(driver):
    """
    Test function to perform the login and verify the dashboard.
    """
    # Find elements and perform actions
    driver.find_element(by=By.NAME, value="username").send_keys("Admin")
    driver.find_element(by=By.NAME, value="password").send_keys("admin123")
    driver.find_element(by=By.CSS_SELECTOR, value="button").click()

    # Verify the current URL and title
    expected_url = "https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index"
    expected_title = "OrangeHRM"

    assert driver.current_url == expected_url
    assert driver.title == expected_title