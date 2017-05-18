import pytest
from flask import json


class TestFlaskPy2Neo(object):

    def test_config(self, db):
        db.graph.run("CREATE (n:TestConfig)")
        op = db.graph.run("MATCH (n:TestConfig) RETURN n")
        assert op.forward()
        assert not op.forward()

    @pytest.mark.xfail
    def test_db_setup(self, db, bolt_db):
        assert 'http' in db.graph.transaction_uri
        assert False

    def test_sample_app_create_get(self, client, db):
        resp = client.get('/create/pika')
        assert resp.status_code == 200

    def test_sample_app_list_get(self, client, db):
        resp = client.get('/list/')
        assert resp.status_code == 200
        resp_json = json.loads(resp.get_data())
        assert resp_json[0]['n']['name'] == 'pika'

    @pytest.mark.xfail
    def test_simple_ogm(self, db):

        class Thing(db.Model):

            title = db.Property()

        thing = Thing()
        thing.title = 'my first post'

        db.graph.push(thing)

        assert False

    def test_ogm_relationships(self, db):

        class Post(db.Model):

            title = db.Property()
            author = db.RelatedFrom("User")

            def __init__(self, title):
                self.title = title

        class User(db.Model):

            name = db.Property()
            posts = db.RelatedTo("Post")

            def __init__(self, name):
                self.name = name

        user = User(name='pika')
        post = Post(title='a blog post')
        user.posts.add(post)
        post.author.add(user)

        # db.graph.push(user)

        assert False