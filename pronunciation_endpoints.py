import os
import uuid

from flask import request, send_file
from flask_restful import Resource

from database import get_user_pronunciation, save_user_pronunciation, remove_user_pronunciation
from google_tts_client import generate_and_save_audio
from utils import generate_audio_file_path


class PronunciationEndpoints(Resource):
    def get(self):
        if 'userId' not in request.form:
            return "userId missing", 400

        user_id = request.form['userId']
        user_pronunciation = get_user_pronunciation(user_id)
        if not user_pronunciation:
            return None, 204

        return send_file(
            generate_audio_file_path(user_pronunciation['audioFileName']), mimetype="audio/mp3", as_attachment=True,
            download_name=f"{user_id}.mp3")

    def post(self):
        if 'userId' not in request.form:
            return "userId missing", 400
        if 'legalFirstName' not in request.form:
            return "legalFirstName missing", 400
        if 'legalLastName' not in request.form:
            return "legalLastName missing", 400

        user_id = request.form['userId']
        legal_first_name = request.form['legalFirstName']
        legal_last_name = request.form['legalLastName']
        preferred_name = request.form['preferredName'] if 'preferredName' in request.form else None
        audio_file = request.files['audio'] if 'audio' in request.files else None

        audio_file_name = str(uuid.uuid4())
        audio_file_path = generate_audio_file_path(audio_file_name)
        if audio_file:
            audio_file.save(audio_file_path)
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
            old_audio_file_path = generate_audio_file_path(old_user_pronunciation['audioFileName'])
            if os.path.exists(old_audio_file_path):
                os.remove(old_audio_file_path)

        return None, 204

    def delete(self):
        if 'userId' not in request.form:
            return "userId missing", 400

        user_id = request.form['userId']
        old_user_pronunciation = remove_user_pronunciation(user_id)
        if old_user_pronunciation:
            old_audio_file_path = generate_audio_file_path(old_user_pronunciation['audioFileName'])
            if os.path.exists(old_audio_file_path):
                os.remove(old_audio_file_path)

        return None, 204
