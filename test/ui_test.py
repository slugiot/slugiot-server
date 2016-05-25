import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

demo_time = 1


class SeleniumTest(unittest.TestCase):

    # This is called before each test
    def setUp(self):
        # TODO: Replace with Chrome
        self.driver = webdriver.Firefox()

    # test log in page redirect to Google
    def test_login(self):

        # let's get to the login page
        self.driver.get('http://127.0.0.1:8000/')
        time.sleep(demo_time)
        self.driver.find_element_by_css_selector('#btn-login').click()
        time.sleep(demo_time)
        print('Redirected to login page successfully')
        time.sleep(demo_time)

        # let's actually login now
        email_element = self.driver.find_element_by_id("auth_user_email")
        email_element.send_keys('blah@blah.com')
        time.sleep(demo_time)
        password_element = self.driver.find_element_by_id("auth_user_password")
        password_element.send_keys('1234')
        time.sleep(demo_time)
        password_element.send_keys(Keys.ENTER)
        time.sleep(demo_time + 1)
        print('Logged in and redirected to dashboard successfully')

        # let's add a device
        add_link = self.driver.find_elements_by_xpath("//*[contains(text(), 'Devices')]")
        print add_link
        add_link[0].click()
        print('Redirected to add device page successfully')
        time.sleep(demo_time)
        name_element = self.driver.find_element_by_id("device_name")
        name_element.send_keys('Selenium Test Device')
        time.sleep(demo_time)
        description_element = self.driver.find_element_by_id("device_description")
        time.sleep(demo_time)
        description_element.send_keys('This device should be deleted when done with testing.')
        description_element.submit()
        time.sleep(demo_time)
        print('Successfully added a device with ID')

        # let's select that device from the sidebar
        self.driver.find_element_by_id("nav-toggle").click()
        time.sleep(demo_time)
        device_link = self.driver.find_elements_by_xpath("//*[contains(text(), 'Selenium Test Device')]")
        device_link[0].click()
        self.driver.find_element_by_id("nav-toggle").click()
        time.sleep(demo_time)
        self.driver.find_element_by_id("btn-procedure").click()
        time.sleep(demo_time + 1)
        self.driver.get('http://127.0.0.1:8000/')
        time.sleep(demo_time)
        self.driver.find_element_by_id("nav-toggle").click()
        time.sleep(demo_time)
        device_link = self.driver.find_elements_by_xpath("//*[contains(text(), 'Selenium Test Device')]")
        device_link[0].click()
        self.driver.find_element_by_id("nav-toggle").click()
        time.sleep(demo_time)
        boo = self.driver.find_elements_by_xpath("//*[contains(text(), 'Edit Device')]")
        boo[0].click()
        time.sleep(demo_time)
        self.driver.get('http://127.0.0.1:8000/')
        self.driver.find_element_by_id("nav-toggle").click()
        time.sleep(demo_time)
        device_link = self.driver.find_elements_by_xpath("//*[contains(text(), 'Selenium Test Device')]")
        device_link[0].click()
        self.driver.find_element_by_id("nav-toggle").click()
        time.sleep(demo_time)
        self.driver.find_element_by_id("btn-delete").click()
        time.sleep(demo_time+1)

    """
    # This works the same as login
    def test_signup(self):
        self.driver.get('https://www.crowdgrader.org')
        time.sleep(demo_time)
        login = self.driver.find_element_by_css_selector('.btn-signup').click()
        current_url = self.driver.current_url
        parsed_uri = urlparse(current_url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        time.sleep(demo_time)
        self.assertEqual('https://accounts.google.com/', domain)
        print('Sign up test passed: redirected to ' + domain)

    def test_follow_link_from_home_page(self):
        self.driver.get('https://www.crowdgrader.org')
        time.sleep(demo_time)
        self.assertEqual('CrowdGrader: Peer Grading for Your Classroom',
                         self.driver.title)  # assert that the home page has title rowdGrader: Peer Grading for Your Classroom'
        print('Page title=' + self.driver.title)
        dropdown_links = self.driver.find_elements_by_class_name(
            'dropdown-toggle')  # the the dropdown menus by css class name
        dropdown_links[2].click()  # click on the second dropdown menu
        time.sleep(1)  # sleep for 1 second so that we make sure the dropdown menu is opened
        self.driver.find_element_by_link_text("Documentation").click()  # click on the link with the text "Documention"
        time.sleep(demo_time)

        # Switch to a new window because the link will open a new window
        from selenium.webdriver.support.wait import WebDriverWait

        # wait to make sure there are two windows open
        WebDriverWait(self.driver, 10).until(lambda d: len(d.window_handles) == 2)

        # switch windows
        self.driver.switch_to_window(self.driver.window_handles[1])

        # wait to make sure the new window is loaded
        WebDriverWait(self.driver, 10).until(lambda d: d.title != "")

        # Assert that to correct URL is loaded by clicking documentation, self.drive.current_url is the current_url
        # we check if it is http://doc.crowdgrader.org/crowdgrader-documentation
        self.assertEqual('http://doc.crowdgrader.org/crowdgrader-documentation', self.driver.current_url)
        print('Current url=' + self.driver.current_url)

        # Find the Testimonial link (by its text) on the new page and click on it
        self.driver.find_element_by_link_text('Testimonials').click()
        time.sleep(demo_time)

        # Check if correct URL is loaded, as above
        self.assertEqual('http://doc.crowdgrader.org/testimonials', self.driver.current_url)
        print('Current url:' + self.driver.current_url)

        # Find a html span element by css id = #sites-page-title
        span = self.driver.find_element_by_id('sites-page-title')

        # Make sure the element has text Testimonials
        self.assertEqual('Testimonials', span.text)
        print('Main text in page:' + span.text)

        # Find the search input field by id
        search_input = self.driver.find_element_by_id('jot-ui-searchInput')

        # Write "text" to the search field
        search_input.send_keys("test")

        time.sleep(demo_time)

        # Find and click the search button
        search_button = self.driver.find_element_by_id('sites-searchbox-search-button')
        search_button.click()

        time.sleep(1)

        # Make sure search button get the correct URL
        self.assertEqual('http://doc.crowdgrader.org/system/app/pages/search?scope=search-site&q=test',
                         self.driver.current_url)
        print('Current url:' + self.driver.current_url)

        time.sleep(1)

        # Make sure search results contains a link to "Privacy Policy"
        result = self.driver.find_element_by_link_text("Privacy Policy")

        # Make sure we can click on Privacy Policy
        result.click()
    """

    # This is called after each test
    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()