"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# esto me ayuda a manejar los errores 
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)




#este codigo es para generar una lista de la familia jackson
#primer endpoint / (GET /members)

@app.route('/members', methods=['GET'])
def get_members():
    member = jackson_family.get_all_members()
    return jsonify(member), 200



#codigo para recuperar/buscar a un familiar (esto es un parametro (<int:id> )que estas usando para buscar en el members id)
#segundo endpoint / (GET /member/<int:member_id>)

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"error": "member no found"}), 404
 
#codigo para agregar un miembro a la familia 
#tercer endpoint / (POST /member)

@app.route('/member', methods= ['POST'])
def add_member(): 
    body = request.get_json()
    new_member = {
        'id': body['id'],
        'first_name': body['first_name'],
        'age': body['age'],
        'lucky_numbers': body['lucky_numbers']
    }
    jackson_family.add_member(new_member)
    response_body = {
        'message': 'successfully added',
        'member': new_member
    }
    return jsonify(response_body), 200
    
    
#vamos a eliminar a un familiar y tambien usamos el mismo parametro del principo , ya que se nesecita los datos y en especial el id  
#cuarto endpoint / (DELETE /member/<int:id>)


@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    jackson_family.delete_member(id)
    return jsonify({'done': True}), 200



    # this is how you can use the Family datastructure by calling its methods
members = jackson_family.get_all_members()




# this only runs if `$ python src/app.py` is executed


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
