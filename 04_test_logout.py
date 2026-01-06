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

    # 1. Hacer clic en el nombre de usuario (Esquina superior derecha)
    # Este elemento despliega el menú oculto
    user_dropdown = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "oxd-userdropdown-name")))
    user_dropdown.click()

    # 2. Esperar a que la opción 'Logout' sea visible y hacer clic
    # Usamos LINK_TEXT porque es una etiqueta <a> con el texto exacto
    logout_link = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Logout")))
    logout_link.click()

    # 3. Validar que volvimos a la página de Login
    # Una forma segura es verificar que el campo de username esté presente de nuevo
    wait.until(EC.presence_of_element_located((By.NAME, "username")))
    
    current_url = driver.current_url
    assert "login" in current_url
    print(f"Logout exitoso en {request.node.name}. URL actual: {current_url}")

    # Tomar captura de pantalla de la página de login post-logout
    import os
    if not os.path.exists("screenshots"): os.makedirs("screenshots")
    driver.save_screenshot(f"screenshots/logout_success_{request.node.name}.png")