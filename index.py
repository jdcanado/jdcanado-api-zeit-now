# app.py
from flask import Flask, jsonify, abort, make_response, request
from flask_restplus import Resource, Api, fields
from werkzeug.contrib.fixers import ProxyFix
from database import db_session
from models import BlogPost
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app,
          version='0.1',
          title='Our sample API',
          description='This is our sample API'
)

db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

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

class Caminhao(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  tipo = db.Column(db.String(100), unique=True)
  
  def __init__(self, tipo):
    self.tipo = tipo
    
# Caminhao Schema
class CaminhaoSchema(ma.Schema):
  class Meta:
    fields = ('id', 'tipo')

# Init schema
caminhao_schema = CaminhaoSchema(strict=True)
caminhoes_schema = CaminhaoSchema(many=True, strict=True)

@app.route('/caminhao', methods=['POST'])
def adicionar_caminhao():
  if not request.json or not 'tipo' in request.json:
        abort(400)

  tipo = request.json['tipo']
  
  novo_caminhao = Caminhao(tipo)
  db.session.add(novo_caminhao)
  db.session.commit()

return caminhao_schema.jsonify(novo_caminhao)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(debug=True)
