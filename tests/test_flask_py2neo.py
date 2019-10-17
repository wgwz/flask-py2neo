import pytest
from flask import json
from py2neo.ogm import GraphObject, Property, RelatedFrom, RelatedTo


class Post(GraphObject):
    title = Property()
    author = RelatedFrom("User")

    def __init__(self, title):
        self.title = title


class User(GraphObject):
    name = Property()
    posts = RelatedTo("Post")

    def __init__(self, name):
        self.name = name


class Thing(GraphObject):
    title = Property()


class TestFlaskPy2Neo(object):
    def test_config(self, db):
        db.graph.run("CREATE (n:TestConfig)")
        op = db.graph.run("MATCH (n:TestConfig) RETURN n")
        assert op.forward()
        assert not op.forward()

    def test_sample_app_create_get(self, client, db):
        resp = client.get("/create/pika")
        assert resp.status_code == 200

    def test_sample_app_list_get(self, client, db):
        resp = client.get("/list/")
        assert resp.status_code == 200
        resp_json = json.loads(resp.get_data())
        assert resp_json[0]["n"]["name"] == "pika"

    def test_simple_ogm(self, db):
        thing = Thing()
        thing.title = "my first post"
        db.graph.push(thing)
        op = db.graph.run("MATCH (n:Thing) RETURN n")
        assert op.forward()
        assert not op.forward()

    def test_ogm_relationships(self, db):
        user = User(name="pika")
        post = Post(title="a blog post")
        user.posts.add(post)
        post.author.add(user)
        db.graph.push(user)
        op = db.graph.run("MATCH (u:User)-[:POSTS]->(p:Post) RETURN u, p")
        assert op.forward()
        assert not op.forward()
