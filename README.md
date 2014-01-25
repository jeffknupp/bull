# `bull` always charges...

## WTF is `bull`?

On a Friday evening, not too long ago, I was lamenting the shortcomings of the
various services I've used to sell my book from my website. Digital goods sales
should be a solved problem by now, but I ran into all sorts of issues when
trying to send updates to customers and integrate properly with Google
Analytics.

[Long story](http://www.jeffknupp.com/blog/2014/01/18/python-and-flask-are-ridiculously-powerful/) short, I 
took two hours and wrote a replacement using Python, Flask, SQLAlchemy, and
Stripe as the payment processor. `bull` is easy enough to set up in a few
minutes *on your own domain*. Why does being on your domain matter? Because it
makes Google Analytics happy and report conversions properly.

The only things you need to get started using `bull` are a Stripe account (free)
and a web server (free?).

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

## Deployment

*Don't run `app.py` in production.* The webserver it uses is not meant for such
a purpose. Instead, deploy as you would normally deploy an WSGI application. See
[Flask's documentation](http://flask.pocoo.org/docs/deploying/) on the subject.

## TODO

A ton. Need to add tests, better documentation, deployment information, good way
to override default templates. All of this is coming. I just wanted to get it
out as fast as possible so that those who know what they're doing can make use
of it.
