Installation
------------

1. ``pip install bull``. This installs the ``bull`` command, which helps
   setup your environment
2. ``bull setup``. This creates a directory named ``bull`` with the
   following contents:

   -  ``app.py``: the main application script. ``get_app`` can be used
      to run ``bull`` as a WSGI application
   -  ``config.py``: ``bull``'s configuration file. This must be edited
      to contain your installation-specific configuration details.
   -  ``files`` directory: The directory that contains the files for
      your digital products

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
