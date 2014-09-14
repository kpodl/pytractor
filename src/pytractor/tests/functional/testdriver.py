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
"""
The webdriver used for most functional tests.
"""

from selenium import webdriver

from pytractor.mixins import WebDriverMixin


class TestDriver(WebDriverMixin, webdriver.Firefox):
    """We use the Firefox driver with our mixin for these tests."""
    pass
