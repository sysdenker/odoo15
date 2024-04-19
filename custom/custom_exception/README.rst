.. image:: https://img.shields.io/badge/license-LGPL--3-green.png
   :target: https://www.gnu.org/licenses/lgpl
   :alt: License: LGPL-3


Custom Exception
================
This modules adds the functionality of Odoo's *UserError*
with a bit of taste from *sweetalert.js* popup notification
style.


Usage
=====
Install the module and import to the file you want to
throw an exception.


Technical Explanation
=====================
The exception requires at least one argument, the *required*
being **error message** as the first argument. The other two are
optional, and in their absence the default value is **error**.

*  argument 1 - *error message* (**NB:** *Must be there others optional*)
*  argument 2 - *title*
*  argument 3 - *icon* must be **error**, **info** or **success**



Code
-----
Example showing code sample having arguments.

All arguments
<<<<<<<<<<<<<
.. image:: /custom_exception/static/images/code.png
    :width: 400px
    :alt: code

Main argument
<<<<<<<<<<<<<
.. figure:: /custom_exception/static/images/code_2.png
    :width: 400px
    :alt: code


Example
-------
.. image:: /custom_exception/static/images/test.gif
    :width: 800px
    :alt: demo


Overwrite Existing UserError
----------------------------
This sample overwrites the *sale.order.line* **unlink** function
to show the exception.

Code
<<<<<
.. image:: /custom_exception/static/images/code_3.png
    :width: 400px
    :alt: code

Example
<<<<<<<

.. image:: /custom_exception/static/images/test.gif
    :width: 800px
    :alt: demo