from flask import Blueprint, request, jsonify
from app.models.anime_model import Anime


bp_animes = Blueprint('animes',__name__, url_prefix='/api')

TABLE_FIELDS = ["anime","released_date","seasons"]

def check_fields_json(data):
    valid_keys = []
    invalid_keys = []

    for item in data.keys():
        if item not in TABLE_FIELDS:
            invalid_keys.append({item: data[item]})
        elif item == "anime" and type(data[item]) == str:
            valid_keys.append({item: data[item]})
        elif item == "released_date" and type(data[item]) == str:
            valid_keys.append({item: data[item]})
        elif item == "seasons" and type(data[item]) == int:
            valid_keys.append({item: data[item]})
        else:
            invalid_keys.append({item: data[item]})

    if invalid_keys != []:
        return {"valid_keys": valid_keys, "invalid_keys": invalid_keys}
    else:
        return None


@bp_animes.route('/animes', methods=['POST', 'GET'])
def get_create():
    if request.method == 'POST':
        data = request.get_json()
        json_not_valid = check_fields_json(data)
        if json_not_valid:
            return json_not_valid, 422
        
        try:
            output = Anime.save(data)
            return jsonify(output), 201
        except:
            return {"msg":'The anime already exists in the database'}, 409

    if request.method == 'GET':
        try:
            return jsonify(Anime.show()), 200
        except TypeError:
            return 'Failed to get data', 400



@bp_animes.route('/animes/<int:anime_id>', methods=['GET'])
def filter(anime_id):
   
    try:
        output = Anime.show_anime_by_id(anime_id)

        return jsonify(output), 200
    except:
        return {"msg": "Anime not found"}, 404


@bp_animes.route('/animes/<int:anime_id>', methods=['PATCH'])
def update(anime_id):
    data = request.get_json()
    json_not_valid = check_fields_json(data)
    if json_not_valid:
        return json_not_valid, 422

    try:
        output = Anime.update(anime_id, data)

        return jsonify(output), 200
    except:
        return {'msg': 'Anime not found'}, 404



@bp_animes.route('/animes/<int:anime_id>', methods=['DELETE'])
def delete(anime_id):
    

    try:
        output = Anime.delete(anime_id)
        if output:
            return "", 204
    except:
        return {'msg': 'Anime not found'}, 404


