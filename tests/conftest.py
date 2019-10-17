from flask import Flask, jsonify
from flask_py2neo import Py2Neo
import pytest


@pytest.fixture(scope="session")
def app():
    """
    Setup the test app context

    :return: Flask app instance
    """
    _app = Flask(__name__)

    with _app.app_context():
        yield _app


@pytest.fixture(scope="session")
def client(app):
    """
    Application client

    :param app: Pytest fixture
    :return: Flask app client
    """
    yield app.test_client()


@pytest.fixture(scope="session")
def bolt_app():
    """
    Setup the test app context

    :return: Flask app instance
    """
    _app = Flask(__name__)

    with _app.app_context():
        yield _app


@pytest.fixture(scope="session")
def bolt_client(bolt_app):
    """
    Application client

    :param app: Pytest fixture
    :return: Flask app client
    """
    yield app.test_client()


def create_views(app, db):
    @app.route("/create/<string:name>")
    def create(name):
        db.graph.run("CREATE (n:User {name: '%s'})" % name)
        return jsonify("user %s created" % name)

    @app.route("/list/")
    def list():
        return jsonify(db.graph.run("MATCH (n:User) RETURN n").data())

    return None


@pytest.fixture(scope="session")
def db(app):

    app.config.update({"PY2NEO_PASSWORD": "test"})

    db = Py2Neo()
    db.init_app(app)

    create_views(app, db)

    yield db

    db.graph.delete_all()


@pytest.fixture(scope="session")
def bolt_db(bolt_app):

    bolt_app.config.update({"PY2NEO_BOLT": True, "PY2NEO_PASSWORD": "test"})

    db = Py2Neo()
    db.init_app(bolt_app)

    create_views(bolt_app, db)

    yield db

    db.graph.delete_all()
