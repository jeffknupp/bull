``bull`` always charges...
==========================

|Build Status| |Coverage Status|

WTF is ``bull``?
----------------

On a Friday evening, not too long ago, I was lamenting the shortcomings
of the various services I've used to sell my digital book from my
personal website. *Digital goods sales should be a solved problem by
now*, but I ran into all sorts of issues when trying to send updates to
customers and integrate properly with Google Analytics.

`Long
story <http://www.jeffknupp.com/blog/2014/01/18/python-and-flask-are-ridiculously-powerful/>`__
short, I took two hours and wrote a replacement using Python, Flask,
SQLAlchemy, and Stripe (as the payment processor). ``bull`` is to set up
*on your own domain*. Why does the fact that ``bull`` runs on your own
domain matter? Because it makes Google Analytics happy and report
conversions properly.

The only things you need to get started using ``bull`` are a Stripe
account (free) and a web server (free?).

Installation
------------

1. ``pip install bull``. This installs the ``bull`` command, which helps
   setup your environment
2. ``bull setup``. This creates a directory named ``bull`` with the
   following contents:

-  ``app.py``: the main application script. ``get_app`` can be used to
   run ``bull`` as a WSGI application
-  ``config.py``: ``bull``'s configuration file. This must be edited to
   contain your installation-specific configuration details.
-  ``files`` directory: The directory that contains the files for your
   digital products

3. Add product entries to the database (use ``scripts/populate_db`` as a
   model)
4. (Optional) Create an admin user for viewing ``/reports`` by running
   ``scripts/create_user.py``
5. Add ``bull`` to your web server's configuration
6. Profit! (...literally)

Analytics and Login
-------------------

``bull`` supports simple sales analytics at the ``/reports`` endpoint.
It requires authorization, which in turn requires you to create (at
least one) user using the ``scripts/create_user.py`` script. To see the
reports, hit ``/login``, log in, and from then on you can go directly to
``/reports`` to see reporting data. You should be good to go after that,
and no one else will be able to see the reports.

If for some reason you need to logout, there is also a ``/logout``
endpoint which will log you out (which should use HTTP POST instead of
GET, but whatever).

**Reporting includes:**

-  Email addresses and sales totals of recent purchases
-  Sales data broken down by calendar day
-  Sales charts based on revenue/units sold per day

Overriding Default Templates
----------------------------

Simply create a ``templates`` directory and create a file of the same
name as the template you want to replace.

Testing
-------

``bull`` has a (small) suite of tests that are run via TravisCI, but can
(and should) also be tested manually once installed. Run
``python app.py`` and browse to http://localhost:5000/test/1. You should
see a single "Buy" button, which should be completely functional
(assuming you have at least one product in your database). Enter
Stripe's test credit card number (4242 4242 4242 4242). You should be
successfully directed to a "success.html" page with your download link.
If your product is in the ``files`` directory, you'll be able to
download it by clicking the link.

Deployment
----------

*Don't run ``app.py`` in production.* The web server it uses is not
meant for such a purpose. Instead, deploy as you would normally deploy
an WSGI application. See `Flask's
documentation <http://flask.pocoo.org/docs/deploying/>`__ on the
subject.

TODO
----

Still need to add better documentation and (possibly) deployment
information. All of this is coming. I just wanted to get ``bull`` out as
fast as possible so that those who know what they're doing can make use
of it.

|Bitdeli Badge|

.. |Build Status| image:: https://travis-ci.org/jeffknupp/bull.png?branch=develop
   :target: https://travis-ci.org/jeffknupp/bull
.. |Coverage Status| image:: https://coveralls.io/repos/jeffknupp/bull/badge.png?branch=develop
   :target: https://coveralls.io/r/jeffknupp/bull?branch=develop
.. |Bitdeli Badge| image:: https://d2weczhvl823v0.cloudfront.net/jeffknupp/bull/trend.png
   :target: https://bitdeli.com/free
