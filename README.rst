=========
pytractor
=========
**Angular.js for the testing goat: Utilities for testing Angular.js applications with Selenium for Python.**

Overview
--------

*pytractor* is an extension to the `Selenium bindings for Python <https://pypi.python.org/pypi/selenium>`_. Its goal is to make testing of angular.js applications easier with Python.

It is built on some parts of `protractor <https://github.com/angular/protractor>`_, the "official" Javascript E2E/Scenario testing framework for `Angular.js <https://angularjs.org/>`_.


Usage
-----

It is assumed that you are familiar with with the `Selenium bindings for Python <https://pypi.python.org/pypi/selenium>`_.

Basics
======

Drivers containing the helper methods for testing Angular.js can be found in the ``pytractor.webdriver`` module.

The constructor expects two parameters: the base URL of your application and the selector for the DOM element which is the root of your Angular.js app.

::

  from pytractor.webdriver import Firefox

  driver = Firefox('http://localhost:8080/base_url', 'body')

The base URL will be prepended to each URL you pass to the ``get()`` method (using ``urlparse.urljoin(base_url, get_url)``).

If no Angular.js app can be found, ``get()`` will raise an exception.

The usual selenium webdriver methods can be used, but pytractor will wait for Angular.js to finish processing for some of them.

Additional methods
==================

Finding Elements
^^^^^^^^^^^^^^^^

Finding elements by binding
+++++++++++++++++++++++++++
The ``find_element(s)_by_binding()`` methods retrieve the element(s) which use the specified binding.

Suppose your Angular app contains a binding of the form

::

  <div>{{my_binding}}</div>

Then you can locate the ``<div />`` with

::

  driver.find_element_by_binding('my_binding')

``find_element(s)_by_binding()`` will also find elements if only part of the binding
name is specified.
In other words, the binding

::

  <div>{{my_binding}}</div>

can be found with

::

  driver.find_element_by_binding('my_bind')


If you want to locate the binding by its **exact** name, use
``find_element(s)_by_exact_binding()``.

Finding elements by model
+++++++++++++++++++++++++
``find_element(s)_by_model('model_name')`` can be used to locate elements that
use the expression ``ng-model="model_name"``.

Suppose you have the element
::

  <input type="text" ng-model="person.name">

then the ``<input>`` element can be found with
::

    driver.find_element_by_model('person.name')


Other Methods and Properties
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Refreshing a page
+++++++++++++++++

``refresh()`` will perform a full reload of the current page. It assumes that
the page uses Angular.js.

Using in-page navigation
++++++++++++++++++++++++

``set_location(url)`` will use the in-page navigation (just as ``$location.url()``).

Retrieving the absolute URL
+++++++++++++++++++++++++++
The ``location_abs_url`` property will retrieve the absolute URL from angular.


Missing Features
----------------

- Button text, repeater, css, and options locators.
- Script/mock module injection.

License
-------

pytractor is licensed under the the Apache License, Version 2.0:
http://www.apache.org/licenses/LICENSE-2.0

protractor is Copyright (c) 2010-2014 Google, Inc. and licensed under the MIT license. See the respective directory for a copy of the license.

Credits
-------
Credits for the client-side scripts go to the `protractor <https://github.com/angular/protractor>`_ project for their fine framework.
