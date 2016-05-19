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

    #initial to insert a procedure into the database
    def test_init(self):
        print("run test_init")
        driver = self.driver
        driver.get("http://127.0.0.1:8000/editor/run_test")
        element = driver.find_element_by_tag_name('body')
        self.assertIn('ok', element.text)


    # test for the save function for unstable procedure
    def test_save(self):
        print("run unstable")
        #get the page with edit button
        driver = self.driver
        driver.get("http://127.0.0.1:8000/editor/unit_test")
        time.sleep(1)
        element = driver.find_element_by_id('unstable')
        element.click()
        time.sleep(1)
        # find and click the save button
        element_save_unstable = driver.find_element_by_id('save_unstable')
        element_save_unstable.click()
        time.sleep(2)
        element_result = driver.find_element_by_id('save_result')
        print(element_result.text)
        self.assertIn('file saved successfully', element_result.text)


    # test for the save function for stable procedure
    def test_save_next(self):
        print("run stable")
        #get the page with edit button
        driver = self.driver
        driver.get("http://127.0.0.1:8000/editor/unit_test")
        time.sleep(1)
        element = driver.find_element_by_id('stable')
        element.click()
        time.sleep(1)
        # find and click the save button
        element_save_stable = driver.find_element_by_id('save_stable')
        element_save_stable.click()
        time.sleep(2)
        element_result = driver.find_element_by_id('save_result')
        print(element_result.text)
        self.assertIn('file saved successfully', element_result.text)

    # get called after every test method
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()