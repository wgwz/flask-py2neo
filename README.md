Flask-Py2Neo
------------

Flask-Py2Neo is mostly a connection utility. The aim is to get you up and running as quickly as possible. It also aims to use best-practices in terms of how the connection is made between py2neo and your Neo4j instance.

Quickstart
----------

Here is a quickstart guide. It shows how to initialize and make use of the extension.

To initialize in an application module:

    from flask import Flask, jsonify
    from flask_py2neo import Py2Neo

    app = Flask(__name__)
    db = Py2Neo(app)

Or this pattern:

    from flask import Flask, jsonify
    from flask_py2neo import Py2Neo

    app = Flask(__name__)
    db = Py2Neo()
    db.init_app(app)

Then define some view functions:

    @app.route('/create/<string:name>')
    def create(name):
        db.graph.run("CREATE (n:User {name: '%s'})" % name) # noqa
        return jsonify('user %s created' % name)

    @app.route('/list/')
    def list():
        return jsonify(db.graph.run("MATCH (n:User) RETURN n").data())

Object-Graph Mapper
-------------------

    from py2neo.ogm import GraphObject, Property

    class Post(GraphObject):

        title = Property()

    post = Post()
    post.title = 'my first post'

    db.graph.push(post)

References
----------

- py2neo v3 Handbook: http://py2neo.org/v3/
- py2neo v4 Handbook: http://py2neo.org/v3/
- py2neo v3 OGM: http://py2neo.org/v3/ogm.html
- py2neo v4 OGM: http://py2neo.org/v3/ogm.html
- py2neo: https://github.com/technige/py2neo
- Flask: https://github.com/pallets/flask

Useful tidbits
--------------

- Cypher Ref Card: https://neo4j.com/docs/cypher-refcard/current/
