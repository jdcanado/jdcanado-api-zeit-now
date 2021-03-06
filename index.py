# app.py
from flask import Flask
from flask_restplus import Resource, Api, fields
from werkzeug.contrib.fixers import ProxyFix
from database import db_session
from models import BlogPost
from models import Caminhao

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app,
          version='0.1',
          title='Our sample API',
          description='This is our sample API'
)

@api.route('/hello_world')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

@api.route('/blog_posts')
class BlogPosts(Resource):
    model = api.model('BlogPost', {
        'id': fields.Integer,
        'title': fields.String,
        'post': fields.String,
    })

    @api.marshal_with(model, envelope='resource')
    def get(self, **kwargs):
        return BlogPost.query.all()

@api.route('/caminhoes')
class Caminhao(Resource):
    model = api.model('Caminhao', {
        'id': fields.Integer,
        'tipo': fields.String,
    })

    @api.marshal_with(model, envelope='resource')
    def get(self, **kwargs):
        return Caminhao.query.all()
    
    @api.expect(model)      
    def post(self):
        caminhao = Caminhao(id = self.id, tipo = self.tipo)            
        db_session.add(caminhao)
        db_session.commit()  

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(debug=True)
