# `Bull` always charges...

## Quickstart

Clone the `bull` repository (or `pip install bull`, if you do this, copy the `app.py` file from 
the repo to whatever directory you want to run it from). Fill in the 
values in `config.py` (use your "test" Stripe keys for now). Create a directory
`files` and add the content you're selling there. Add product entries to your database with the 
appropriate filename (use `scripts/populate_db` as a model).

## Analytics and Login

`bull` now supports simple sales analytics at the `/reports` endpoint. It
requires authorization, which in turn requires you to create (one) user using
the `scripts/create_user.py` script. To see the reports, hit `/login` and log
in. You should be good to go after that, and no one else will be able to see the
reports.

**Reporting includes:**

* Email addresses and sales totals of recent purchases
* Sales data broken down by calendar day
* Sales charts based on revenue/units sold per day

## Overriding Default Templates

Simply create a `templates` directory and create a file of the same name as the
template you want to replace.

## Testing

Test by running `python app.py` and browsing to [http://localhost:5000/test/1](http://localhost:5000/test/1).
You should see a single "Buy" button, which should be completely functional.
Enter Stripe's test credit card number (4242 4242 4242 4242). You should be
successfully directed to a "success.html" page with your download link. If your
product is in the `files` directory.

## Customizing

For now, directly edit the templates in the `templates` directory to include any
additional content you'd like.

## Deployment

*Don't run `app.py` in production.* The webserver it uses is not meant for such
a purpose. Instead, deploy as you would normally deploy an WSGI application. See
[Flask's documentation](http://flask.pocoo.org/docs/deploying/) on the subject.

## TODO

A ton. Need to add tests, better documentation, deployment information, good way
to override default templates. All of this is coming. I just wanted to get it
out as fast as possible so that those who know what they're doing can make use
of it.
