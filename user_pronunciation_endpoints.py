from flask import request, send_file
from flask_restful import Resource

from database import get_user_pronunciation, save_user_pronunciation, remove_user_pronunciation
from utils import get_audio_file_path


class UserPronunciationEndpoints(Resource):
    def get(self):
        if 'userId' not in request.form:
            return "userId missing", 400

        user_id = request.form['userId']
        user_pronunciation = get_user_pronunciation(user_id)
        if not user_pronunciation:
            return None, 204

        return send_file(
            get_audio_file_path(user_id), mimetype="audio/mp3", as_attachment=True,
            download_name=f"{user_id}.mp3")

    def post(self):
        if 'userId' not in request.form:
            return "userId missing", 400
        if 'name' not in request.form:
            return "name missing", 400
        if 'audio' not in request.files:
            return "audio missing", 400

        user_id = request.form['userId']
        name = request.form['name']
        audio_file = request.files['audio']

        audio_file.save(get_audio_file_path(user_id))

        save_user_pronunciation(user_id, name)
        return None, 204

    def delete(self):
        if 'userId' not in request.form:
            return "userId missing", 400

        user_id = request.form['userId']
        remove_user_pronunciation(user_id)
        return None, 204
