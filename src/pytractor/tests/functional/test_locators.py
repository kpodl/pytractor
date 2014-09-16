# encoding: utf-8
# Copyright 2014 Konrad Podloucky
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest import TestCase

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from .testdriver import TestDriver
from .testserver import SimpleWebServerProcess


class LocatorTestCase(TestCase):
    """Test case class for testing locators."""
    driver = None

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
        self.driver.get('index.html#/form')


class ByBindingLocatorTest(LocatorTestCase):
    """Tests the locators of the WebDriverMixin that deal with bindings."""

    def test_find_element_by_binding_raises_error_if_no_element_matches(self):
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_binding('no-such-binding')

    def test_find_element_by_binding_returns_correct_element(self):
        element = self.driver.find_element_by_binding('greeting')
        self.assertIsInstance(element, WebElement)
        self.assertEqual(element.text, 'Hiya')

    def test_find_element_by_binding_finds_element_by_partial_name(self):
        element = self.driver.find_element_by_binding('greet')
        self.assertIsInstance(element, WebElement)
        self.assertEqual(element.text, 'Hiya')

    def test_find_element_by_binding_finds_element_with_ng_bind(self):
        element = self.driver.find_element_by_binding('username')
        self.assertIsInstance(element, WebElement)
        self.assertEqual(element.text, 'Anon')

    def test_find_element_by_binding_finds_element_with_ng_bind_template(self):
        element = self.driver.find_element_by_binding('nickname|uppercase')
        self.assertIsInstance(element, WebElement)
        self.assertEqual(element.text, '(ANNIE)')

    def test_find_element_by_exact_binding_finds_correct_element(self):
        element = self.driver.find_element_by_exact_binding('greeting')
        self.assertIsInstance(element, WebElement)
        self.assertEqual(element.text, 'Hiya')

    def test_find_element_by_exact_binding_needs_complete_binding_name(self):
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_exact_binding('greet')


class ByModelLocatorTest(LocatorTestCase):
    def test_find_element_by_model_finds_element_by_text_input_model(self):
        username = self.driver.find_element_by_model('username')
        name = self.driver.find_element_by_binding('username')

        username.clear()
        self.assertEqual(name.text, '')

        username.send_keys('Jane Doe')
        self.assertEqual(name.text, 'Jane Doe')

        username.clear()
        self.assertEqual(name.text, '')

    def test_find_element_by_model_finds_element_by_checkbox_input_model(self):
        shower = self.driver.find_element_by_id('shower')
        self.assertTrue(shower.is_displayed())

        colors = self.driver.find_element_by_model('show')
        colors.click()

        shower = self.driver.find_element_by_id('shower')
        self.assertFalse(shower.is_displayed())

    def test_find_element_by_model_finds_textarea_by_model(self):
        about = self.driver.find_element_by_model('aboutbox')
        self.assertEqual(about.get_attribute('value'), 'This is a text box')

        about.clear()
        about.send_keys('Something else to write about')

        self.assertEqual(about.get_attribute('value'),
                         'Something else to write about')

    def test_find_elements_by_model_find_multiple_selects_by_model(self):
        selects = self.driver.find_elements_by_model('dayColor.color')

        self.assertEqual(len(selects), 3)

    def test_find_element_by_model_finds_the_selected_option(self):
        select = self.driver.find_element_by_model('fruit')
        selected_option = select.find_element_by_css_selector('option:checked')

        self.assertEqual(selected_option.text, 'apple')

    def test_find_element_by_model_finds_inputs_with_alternate_attribute_forms(
        self
    ):
        letter_list = self.driver.find_element_by_id('letterlist')
        self.assertEqual(letter_list.text, '')

        self.driver.find_element_by_model('check.w').click()
        self.assertEqual(letter_list.text, 'w')

        self.driver.find_element_by_model('check.x').click()
        self.assertEqual(letter_list.text, 'wx')

    def test_find_elements_by_model_finds_multiple_inputs(self):
        inputs = self.driver.find_elements_by_model('color')

        self.assertEqual(len(inputs), 3)
