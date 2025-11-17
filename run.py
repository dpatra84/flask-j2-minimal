from app import app
from argparse import ArgumentParser
from logging import getLogger
import sys

logger = getLogger(__name__)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--migrate", action="store_true")
    args = parser.parse_args()

    if args.migrate:
        from app.models import db
        with app.app_context():
            db.create_all()
            logger.info("Database tables created.")
            sys.exit(0)
        
    app.run()
