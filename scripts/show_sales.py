import argparse
import datetime
import sys

from flask import current_app
from bull import app, db, Product, Purchase

def main(args):
    """Main entry point for script."""
    today = datetime.date.today()
    if args.all:
        with app.app_context():
            purchases = Purchase.query.all()
            sales = sum(p.product.price for p in purchases)
            for purchase in purchases:
                print str(purchase), purchase.sold_at
            print '{} sales in that period'.format(len(purchases))
            print '${} in total sales in that period'.format(sales)
            return

    if args.today:
        threshold = today - datetime.timedelta(days=1)
    elif args.yesterday:
        threshold = today - datetime.timedelta(days=2)
    elif args.week:
        threshold = today - datetime.timedelta(days=7)
    with app.app_context():
        purchases = Purchase.query.filter(Purchase.sold_at>threshold).all()
        sales = sum(p.product.price for p in purchases)
        for purchase in purchases:
            print str(purchase), purchase.sold_at
        print '{} sales in that period'.format(len(purchases))
        print '{} in total sales in that period'.format(sales)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    with app.app_context():
        current_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite+pysqlite:////Users/jknupp/code/github_code/bull/sqlite3.db'
        db.init_app(current_app)
    parser.add_argument('-t', '--today', help='Get today\'s stats', action='store_true')
    parser.add_argument('-w', '--week', help='Get seven days stats', action='store_true')
    parser.add_argument('-y', '--yesterday', help='Get yesterday\'s stats', action='store_true')
    parser.add_argument('-a', '--all', help='Get all purchases', action='store_true')
    sys.exit(main(parser.parse_args()))
