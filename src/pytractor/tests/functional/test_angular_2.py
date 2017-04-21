from unittest import TestCase

from pytractor.tests.functional import SimpleWebServerProcess
from pytractor.tests.functional.testdriver import TestDriver


class Angular2Test(TestCase):
    """Test case class for testing angular 2."""

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
        self.driver.get('/ng2/#/async')

    def _assert_click(self, scope, button, value):
        val = scope.find_element_by_class_name('val')
        self.assertEqual(val.text, '0')
        button.click()
        self.assertEqual(val.text, value)

    def _assert_click_without_sync(self, scope, button):
        self.driver.ignore_synchronization = True
        val = scope.find_element_by_class_name('val')
        self.assertEqual(val.text, '0')
        button.click()

        import time  # wee need to wait some time for counter change
        time.sleep(10)

        self.driver.find_element_by_button_text('Cancel').click()
        self.assertNotEqual(val.text, '0')

    def test_should_wait_for_increment(self):
        button = self.driver.find_element_by_button_text('Increment')
        scope = self.driver.find_element_by_id('increment')
        self._assert_click(scope, button, '1')

    def test_should_wait_for_delayed_increment(self):
        button = self.driver.find_element_by_button_text('Delayed Increment')
        scope = self.driver.find_element_by_id('delayedIncrement')
        self._assert_click(scope, button, '1')

    def test_should_wait_for_10_delayed_increment(self):
        button = self.driver.find_element_by_button_text('10 Delayed Increments')
        scope = self.driver.find_element_by_id('chainedDelayedIncrements')
        self._assert_click(scope, button, '10')

    def test_should_wait_for_periodic_increment(self):
        button = self.driver.find_element_by_button_text('Periodic Increment')
        scope = self.driver.find_element_by_id('periodicIncrement')
        self._assert_click_without_sync(scope, button)

    def test_should_wait_for_periodic_increment_outsideNgZone(self):
        button = self.driver.find_element_by_button_text('Periodic Increment (outside NgZone)')
        scope = self.driver.find_element_by_id('periodicIncrement_unzoned')
        self._assert_click_without_sync(scope, button)

