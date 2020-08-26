import pytest
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@pytest.fixture(scope="class")
def driver_init(request):
    from selenium import webdriver
    web_driver = webdriver.Chrome(ChromeDriverManager().install())
    request.cls.driver = web_driver
    yield
    # web_driver.close()


@pytest.mark.usefixtures("driver_init")
class BaseTest:
    pass

class TestBooking(BaseTest):

    def timer_wait(self):
        time.sleep(5)

    @pytest.mark.parametrize("url", ["https://www.aldoshoes.com/"])
    def test_select_products(self, url):
        wait = WebDriverWait(self.driver, 3)
        self.driver.get(url)
        wait.until(EC.visibility_of_element_located((By.XPATH,"//button[@id='regular-menu-caenmen']//*[contains(text(),'Men')]"))).click()

    # def test_validate_selclea

    """ below value can be changed to try different combinations of filters if you need choose 5 filters keep 5 in the value"""
    @pytest.mark.parametrize("value", [4])
    def test_validate_selected_filter_combinations(self, value):
        """
        With the help of @pytest.mark.parametrize I have followed a data-driven approach and execute tests on different data sets.
        
        """

        xpaths = ["//label[contains(text(),'Bags & wallets')]", "//label[contains(text(),'Belts')]", "//label[contains(text(),'Face Masks')]",
        "//label[contains(text(),'Hats, gloves & scarves')]", "//label[contains(text(),'Jewelry')]]","//label[contains(text(),'Socks')]"]
        
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//span[text()='accessories']"))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//span[text()='Filter']"))).click()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div#category-control>div"))).click()

        print("waiting till the page gets loaded! Testing Filter combinations")
        self.timer_wait()
        for xpath in xpaths[:value]:
            wait.until(EC.visibility_of_element_located((By.XPATH, f"{xpath}"))).click()
            self.timer_wait()

        print("")
        wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@class='u-btn u-btn--primary c-filters-overlay-controls__apply-btn']"))).click()
        text = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Filter')]"))).text
        items = [int(s) for s in text.split() if s.isdigit()][0]
        assert items == value

