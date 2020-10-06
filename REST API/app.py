from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Init db
db = SQLAlchemy(app)
#init ma
ma = Marshmallow(app)

#Product Class/Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(500))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self,name,description,price,qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

#product schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id','name','description','price','qty')

#Init Schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)



#home
@app.route('/',methods=['GET'])
def home():
    return jsonify({"msg":"hello world"})

#create a product
@app.route('/product',methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name,description,price,qty)

    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)

#get Products
@app.route('/product',methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

@app.route('/product/<id>',methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

#update a product
@app.route('/product/<id>',methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)

    if 'name' in request.json:
        product.name = request.json['name']
    if 'description' in request.json:
        product.description = request.json['description']
    if 'price' in request.json:
        product.price = request.json['price']
    if 'qty' in request.json:
        product.qty = request.json['qty']

    db.session.commit()
    return product_schema.jsonify(product)

#Delete a product
@app.route('/product/<id>',methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)

    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)

#run server
if __name__ == '__main__':
    app.run(debug=True)
