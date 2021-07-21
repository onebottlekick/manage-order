from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# db.create_all()

class OrderModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(100), nullable=False)
    order_date = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'Order(name = {name}, content = {content}, order_date = {order_date})'


order_put_args = reqparse.RequestParser()
order_put_args.add_argument('name', type=str, help='input store name', required=True)
order_put_args.add_argument('content', type=str, help='input content', required=True)
order_put_args.add_argument('order_date', type=str, help='input order date', required=True)

order_update_args = reqparse.RequestParser()
order_update_args.add_argument('name', type=str, help='input store name')
order_update_args.add_argument('content', type=str, help='input content')
order_update_args.add_argument('order_date', type=str, help='input order date')

resource_fields = {
    'id' : fields.Integer,
    'name' : fields.String,
    'content' : fields.String,
    'order_date' : fields.String
}

class Order(Resource):
    @marshal_with(resource_fields)
    # def get(self, order_id):
    #     result = OrderModel.query.filter_by(id=order_id).first()
    def get(self):
        # result = OrderModel.query.filter_by(id=order_id).first()
        result = OrderModel.query.all()
        if not result:
            abort(404, message='order not found...')
        return result
    
    @marshal_with(resource_fields)
    # def put(self, order_id):
    def put(self):
        args = order_put_args.parse_args()
        # result = OrderModel.query.filter_by(id=order_id).first()
        # if result:
        #     abort(409, message='order id taken...')
        # order = OrderModel(id=order_id, name=args['name'], content=args['content'], order_date=args['order_date'])
        order = OrderModel(name=args['name'], content=args['content'], order_date=args['order_date'])
        db.session.add(order)
        db.session.commit()
        return order, 201

    @marshal_with(resource_fields)
    # def patch(self, order_id):
    def patch(self):
        args = order_update_args.parse_args()
        # result = OrderModel.query.filter_by(id=order_id).first()
        result = OrderModel.query.all()
        if not result:
            abort(404, message='order not found, cannot update')
        if args['name']:
            result.name = args['name']
        if args['content']:
            result.name = args['content']
        if args['order_date']:
            result.name = args['order_date']
        
        db.session.commit()

        return result
    
    # def delete(self, order_id):
        


# api.add_resource(Order, '/order/<int:order_id>')
api.add_resource(Order, '/order')

if __name__ == '__main__':
    app.run(debug=True)
