import uuid

from flask import request, send_file
from flask_restful import Resource

from database import get_user_pronunciation, save_user_pronunciation, remove_user_pronunciation
from google_storage_client import save_pronunciation, get_pronunciation, delete_pronunciation
from google_tts_client import generate_and_save_audio
from utils import generate_audio_file_path


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

            audio_file_name = str(uuid.uuid4())
            audio_file_path = generate_audio_file_path(audio_file_name)
            if audio_file:
                save_pronunciation(audio_file_name, audio_file_path)
            else:
                try:
                    name = preferred_name if preferred_name else f'{legal_first_name} {legal_last_name}'
                    generate_and_save_audio(name, audio_file_path)
                except Exception as e:
                    print('Unexpected error', e)
                    return f'Unexpected Error, {str(e)}', 500

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
