from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)




class Messages(Resource):
    def get(self):
        mess_dict = [m.to_dict() for m in Message.query.order_by(Message.created_at).all()]

        response = make_response(jsonify(mess_dict), 200)
        return response
    
    def post(self):
        data = request.get_json()
        new_mess = Message( body = data['body'], username = data['username'])
        db.session.add(new_mess)
        db.session.commit()
        mess_dict = new_mess.to_dict()
        response = make_response(jsonify(mess_dict), 201)
        return response

api.add_resource(Messages, '/messages')

# @app.route('/messages')
# def messages():
#     return ''

# @app.route('/messages/<int:id>')
# def messages_by_id(id):
#     return ''

class MessageById(Resource):
    def patch(self, id):
        data = request.get_json()
        message = Message.query.filter(Message.id == id).first()
        for attr in data:
            setattr(message, attr, data[attr])

        db.session.commit()

        response = make_response(jsonify(message.to_dict()), 200)
        return response

    def delete(self, id):
        message = Message.query.filter(Message.id == id).first()

        db.session.delete(message)
        db.session.commit()

        response = make_response(jsonify({'mesage': f'Message with id:{id} has been deleted'}), 200)
        return response

api.add_resource(MessageById, '/messages/<int:id>')

if __name__ == '__main__':
    app.run(port=4000, debug=True)
