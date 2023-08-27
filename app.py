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


@app.route('/products', methods=['GET', 'POST'])
@app.route('/products/<id>', methods=['GET', 'PUT', 'DELETE'])
def products(id=None):
    if request.method == 'GET':
        if id:
            try:
                return jsonify(model_to_dict(Product.get(Product.id == id)))

            except DoesNotExist:
                return jsonify({'message': f'Product with id {id} not found'})

        else:
            products = []

            for product in Product.select():
                products.append(model_to_dict(product))

            return jsonify(products)

    elif request.method == 'POST':
        new_product = dict_to_model(Product, request.get_json())
        new_product.save()
        return jsonify(model_to_dict(new_product))

    elif request.method == 'PUT':
        Product.update(request.get_json()).where(Product.id == id).execute()
        return jsonify(model_to_dict(Product.get(Product.id == id)))

    elif request.method == 'DELETE':
        Product.delete().where(Product.id == id).execute()
        return jsonify({'message': f'Product with id {id} deleted'})


app.run(port=3030, debug=True)
