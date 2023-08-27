from flask import Flask, request, jsonify
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model
from products import products

db = PostgresqlDatabase('fake_store', user='fake_store_admin',
                        password='fakestoreadmin', host='localhost', port=5432)


class BaseModel(Model):
    class Meta:
        database = db


class Product(BaseModel):
    title = CharField()
    price = FloatField()
    description = CharField(max_length=1000)
    category = CharField()
    image = CharField()
    rating = FloatField()
    rate_count = IntegerField()


db.connect()
db.drop_tables([Product])
db.create_tables([Product])

for product in products:
    Product(
        title=product['title'],
        price=product['price'],
        description=product['description'],
        category=product['category'],
        image=product['image'],
        rating=product['rating']['rate'],
        rate_count=product['rating']['count']
    ).save()

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({'message': 'This is the API root!'})


@app.route('/products')
@app.route('/products/<id>')
def products(id=None):
    if id:
        return jsonify(model_to_dict(Product.get(Product.id == id)))

    else:
        products = []

        for product in Product.select():
            products.append(model_to_dict(product))

        return jsonify(products)


app.run(port=3030, debug=True)
