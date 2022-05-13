import os
import uuid

from flask import request, send_file
from flask_restful import Resource

from database import get_user_pronunciation, save_user_pronunciation, remove_user_pronunciation
from google_storage_client import save_pronunciation, get_pronunciation, delete_pronunciation
from google_tts_client import generate_audio


class PronunciationEndpoints(Resource):
    def get(self):
        if 'userId' not in request.args:
            return "userId missing", 400

        try:
            user_id = request.args['userId']
            user_pronunciation = get_user_pronunciation(user_id)
            if not user_pronunciation:
                return None, 204

            return send_file(
                get_pronunciation(user_pronunciation['audioFileName']), mimetype="audio/mp3", as_attachment=True,
                download_name=f"{user_id}.mp3")
        except Exception as e:
            print('Unexpected error', e)
            return f'Unexpected Error, {str(e)}', 500

    def post(self):
        if 'userId' not in request.form:
            return "userId missing", 400
        if 'legalFirstName' not in request.form:
            return "legalFirstName missing", 400
        if 'legalLastName' not in request.form:
            return "legalLastName missing", 400

        try:
            user_id = request.form['userId']
            legal_first_name = request.form['legalFirstName']
            legal_last_name = request.form['legalLastName']
            preferred_name = request.form['preferredName'] if 'preferredName' in request.form else None
            audio_file = request.files['audio'] if 'audio' in request.files else None

            audio_file_name = f'{str(uuid.uuid4())}.mp3'
            audio_file_path = f'{os.path.join(os.getcwd(), "recordings", audio_file_name)}.mp3'
            if audio_file:
                audio_file.save(audio_file_path)
            else:
                name = preferred_name if preferred_name else f'{legal_first_name} {legal_last_name}'
                generate_audio(name, audio_file_path)

            save_pronunciation(audio_file_name, audio_file_path)

            old_user_pronunciation = save_user_pronunciation(user_id, legal_first_name, legal_last_name, preferred_name,
                                                             audio_file_name)
            if old_user_pronunciation:
                delete_pronunciation(old_user_pronunciation['audioFileName'])

            return None, 204
        except Exception as e:
            print('Unexpected error', e)
            return f'Unexpected Error, {str(e)}', 500

    def delete(self):
        if 'userId' not in request.form:
            return "userId missing", 400

        try:
            user_id = request.form['userId']
            old_user_pronunciation = remove_user_pronunciation(user_id)
            if old_user_pronunciation:
                delete_pronunciation(old_user_pronunciation['audioFileName'])

            return None, 204
        except Exception as e:
            print('Unexpected error', e)
            return f'Unexpected Error, {str(e)}', 500
