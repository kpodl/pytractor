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


class WebDriverLocatorsTest(TestCase):
    """Tests the locators of the WebDriverMixin."""
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

    def test_find_element_by_binding_no_element(self):
        self.driver.get('index.html#/form')
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_binding('no-such-binding')

    def test_find_element_by_binding(self):
        self.driver.get('index.html#/form')
        element = self.driver.find_element_by_binding('greeting')
        self.assertIsInstance(element, WebElement)
        self.assertEqual(element.text, 'Hiya')

    def test_find_element_by_partial_binding(self):
        self.driver.get('index.html#/form')
        element = self.driver.find_element_by_binding('greet')
        self.assertIsInstance(element, WebElement)
        self.assertEqual(element.text, 'Hiya')
