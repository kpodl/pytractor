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

"""
Simple tests for Firefox and Chrome drivers. We just see if the drivers can
be instantiated and run a simple test.
"""
import unittest

from selenium.webdriver.remote.webelement import WebElement

# pylint: disable=no-name-in-module
from pytractor.webdriver import Firefox, Chrome
# pylint: enable=no-name-in-module

from . import SimpleWebServerProcess


class WebDriverTestBase(object):
    driver_class = None
    driver = None

    @classmethod
    def setUpClass(cls):
        cls.driver = cls.driver_class(
            'http://localhost:{}/'.format(SimpleWebServerProcess.PORT),
            'body'
        )

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_find_element_by_binding(self):
        self.driver.get('index.html#/form')
        element = self.driver.find_element_by_binding('greeting')
        self.assertIsInstance(element, WebElement)
        self.assertEqual(element.text, 'Hiya')


class FirefoxWebDriverTest(WebDriverTestBase, unittest.TestCase):
    driver_class = Firefox


class ChromeWebDriverTest(WebDriverTestBase, unittest.TestCase):
    driver_class = Chrome
