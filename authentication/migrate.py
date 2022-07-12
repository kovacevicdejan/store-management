from flask import Flask
from configuration import Configuration
from flask_migrate import Migrate, init, migrate, upgrade
from models import database, User, Role, UserRole
from sqlalchemy_utils import database_exists, create_database

application = Flask(__name__)
application.config.from_object(Configuration)
migrate_object = Migrate(application, database)
done = False

while not done:
    try:
        if not database_exists(application.config["SQLALCHEMY_DATABASE_URI"]):
            create_database(application.config["SQLALCHEMY_DATABASE_URI"])

        database.init_app(application)

        with application.app_context() as context:
            init()
            migrate(message="Production migration")
            upgrade()

            admin_role = Role(name="admin")
            manager_role = Role(name="manager")
            customer_role = Role(name="customer")

            database.session.add(admin_role)
            database.session.add(manager_role)
            database.session.add(customer_role)
            database.session.commit()

            admin = User(email="admin@admin.com", password="1", forename="admin", surname="admin")
            database.session.add(admin)
            database.session.commit()

            user_role = UserRole(user_id=admin.id, role_id=admin_role.id)
            database.session.add(user_role)
            database.session.commit()
            done = True
    except Exception as error:
        print(error)
