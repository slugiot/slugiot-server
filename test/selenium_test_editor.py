import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# inherited from unittest.TestCase
# so that can tell unittest module this is a test case
class EditorTest(unittest.TestCase):

    # get called before every test function in this class
    def setUp(self):
        # create instance of Firefox WebDriver
        self.driver = webdriver.Firefox()

    def test_temp_save(self):
        # local reference to the driver object
        driver = self.driver
        driver.get("http://localhost:8000/editor/test_edit?procedure_id=1&stable=false")
        time.sleep(2)
        # locate the temporary save button
        element = driver.find_element_by_class_name("btn-primary")
        element.click()
        # wait until saved
        time.sleep(2)
        self.assertIn("file saved successfully", driver.page_source)

    def test_stable_save_success(self):
        driver = self.driver
        driver.get("http://localhost:8000/editor/test_edit?procedure_id=1&stable=false")
        time.sleep(2)
        # locate the stable save button
        element = driver.find_element_by_class_name("btn-info")
        element.click()
        # wait until saved
        time.sleep(2)
        self.assertIn("file saved successfully", driver.page_source)

    def test_stable_save_fail(self):
        driver = self.driver
        driver.get("http://localhost:8000/editor/test_edit?procedure_id=1&stable=false")
        time.sleep(2)

        # TODO:
        # locate the editor area
        # use .send_keys("") method add some code in editor area
        # add syntax error code intentionally

        # locate the stable save button
        element = driver.find_element_by_class_name("btn-info")
        element.click()
        # wait until saved
        time.sleep(2)
        self.assertIn("SyntaxError", driver.page_source)


    # get called after every test method
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()