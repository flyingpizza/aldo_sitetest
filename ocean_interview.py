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

    @pytest.mark.parametrize("url", ["https://www.amazon.ca/"])
    def test_select_products(self, url):
        wait = WebDriverWait(self.driver, 3)
        self.driver.get(url)
        wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@id='twotabsearchtextbox']"))).click()

    # def test_validate_selclea
    @pytest.mark.parametrize("value", ['Teddy bear'])
    def test_validate_selected_filter_combinations(self, value):
        """
        With the help of @pytest.mark.parametrize I have followed a data-driven approach and execute tests on different data sets.
        
        """
    
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='twotabsearchtextbox']"))).send_keys(value)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@id='nav-search-submit-text']//input[@class='nav-input']"))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//li[@id='p_72/11192170011']//section"))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'5 to 7 Years')]"))).click()
        print('waiting for timer')
        self.timer_wait()
        wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Melissa & Doug Teddy Bear 60cm Large Soft Toy')]"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='add-to-cart-button']"))).click()
        self.timer_wait()
        for i in range(2):
            self.driver.back()
        
        wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Orb Factory Plush Craft Teddy Bear Pillow Kit')]"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='add-to-cart-button']"))).click()
        self.timer_wait()

        wait.until(EC.presence_of_element_located((By.XPATH, "//a[@id='hlb-view-cart-announce']"))).click()
    
        total = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//form[1]/div[2]//div[4]/div[1]")))

        print("using assert to compare the totol items in the cart")
        assert (len(total)-1) == 2
