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
Unit tests for pytractor.webdriver
"""
from importlib import import_module
import unittest

from selenium import webdriver

from pytractor.mixins import WebDriverMixin


class WebDriverModuleTest(unittest.TestCase):
    # All known webdrivers
    WEBDRIVERS = ['Android', 'Chrome', 'Firefox', 'Ie', 'Opera', 'PhantomJS',
                  'Remote', 'Safari']

    def setUp(self):
        self.module = import_module('pytractor.webdriver')

    def test_module_exports_all_webdrivers(self):
        for driver_name in self.WEBDRIVERS:
            self.assertTrue(
                hasattr(self.module, driver_name),
                '{} was not found in the module!'.format(driver_name)
            )

    def test_exported_webdrivers_are_classes(self):
        for driver_name in self.WEBDRIVERS:
            klass = getattr(self.module, driver_name)
            self.assertIsInstance(
                klass, type, '{} is not a class!'.format(driver_name)
            )

    def test_exported_webdrivers_are_subclasses_of_webdriver_and_mixin(self):
        for driver_name in self.WEBDRIVERS:
            selenium_driver = getattr(webdriver, driver_name)
            pytractor_driver = getattr(self.module, driver_name)
            self.assertTrue(issubclass(pytractor_driver, selenium_driver),
                            'pytractor.webdriver.{0} is not a subclass of '
                            'selenium.webdriver.{0}'.format(driver_name))
            self.assertTrue(issubclass(pytractor_driver, WebDriverMixin),
                            'pytractor.webdriver.{} is not a subclass of '
                            'pytractor.mixins.WebDriverMixin'
                            .format(driver_name))
