import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class EditorTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_temp_save(self):
        driver = self.driver
        driver.get("http://localhost:8000/editor/test_edit?procedure_id=1&stable=false")
        # assert "Server" in driver.title
        time.sleep(2)
        element = driver.find_element_by_class_name("btn-primary")
        element.click()
        hint = driver.find_element_by_class_name("list-group-item")
        self.assertIn("file saved successfully", driver.page_source)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()