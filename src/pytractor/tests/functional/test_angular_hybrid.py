from unittest import TestCase

from pytractor.tests.functional import SimpleWebServerProcess
from pytractor.tests.functional.testdriver import TestDriver


class AngularHybridTest(TestCase):
    """Test case class for testing angular hybrid."""

    @classmethod
    def setUpClass(cls):
        cls.driver = TestDriver(
            'http://localhost:{}/'.format(SimpleWebServerProcess.PORT),
            'body'
        )

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get('/hybrid/')

    def _assert_button_click(self, section):
        button = section.find_element_by_tag_name('button')
        self.assertEqual(button.text, 'Click Count: 0')

        button.click()
        self.assertEqual(button.text, 'Click Count: 1')

    def test_should_click_my_app(self):
        section = self.driver.find_element_by_tag_name('my-app')
        self._assert_button_click(section)

    def test_should_click_ng2(self):
        section = self.driver.find_element_by_tag_name('ng2')
        self._assert_button_click(section)

    def test_should_click_ng1(self):
        section = self.driver.find_element_by_tag_name('ng1')
        self._assert_button_click(section)
