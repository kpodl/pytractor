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
Selenium webdrivers with added angular.js awareness.
"""

from selenium import webdriver as selenium_webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from .mixins import WebDriverMixin

module_dict = globals()  # pylint: disable=invalid-name
__all__ = []

# build classes derived from selenium webdrivers and our WebDriverMixin
for name in dir(selenium_webdriver):
    export = getattr(selenium_webdriver, name)
    if isinstance(export, type) and issubclass(export, WebDriver):
        module_dict[name] = type(name, (WebDriverMixin, export), {})
        __all__.append(name)

__all__ = tuple(__all__)
