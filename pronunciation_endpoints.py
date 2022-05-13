import io
import uuid

from flask import request, send_file
from flask_restful import Resource

from database import *
from google_storage_client import *
from google_tts_client import *
from utils import create_logger

logger = create_logger(__name__)


class PronunciationEndpoints(Resource):
    def get(self):
        if 'userId' not in request.args:
            return "userId missing", 400

        try:
            user_id = request.args['userId']
            user_pronunciation = get_user_pronunciation(user_id)
            if not user_pronunciation:
                return None, 204

            saved_pronunciation_audio = io.BytesIO(
                get_pronunciation_audio_as_string(user_pronunciation['audioFileName']))

            return send_file(
                saved_pronunciation_audio, mimetype="audio/mp3", as_attachment=True,
                download_name=f"{user_id}.mp3")
        except Exception as e:
            logger.exception("Error occurred while getting pronunciation")
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
            if audio_file:
                audio_file_byte_array = io.BytesIO()
                audio_file.save(audio_file_byte_array)
                save_pronunciation_audio_from_string(audio_file_name, audio_file_byte_array.getvalue())
            else:
                name = preferred_name if preferred_name else f'{legal_first_name} {legal_last_name}'
                generated_audio_byte_array = generate_audio(name)
                save_pronunciation_audio_from_string(audio_file_name, generated_audio_byte_array)

            old_user_pronunciation = save_user_pronunciation(user_id, legal_first_name, legal_last_name, preferred_name,
                                                             audio_file_name)
            if old_user_pronunciation:
                delete_pronunciation_audio(old_user_pronunciation['audioFileName'])

            return None, 204
        except Exception as e:
            logger.exception("Error occurred while posting pronunciation")
            return f'Unexpected Error, {str(e)}', 500

    def delete(self):
        if 'userId' not in request.form:
            return "userId missing", 400

        try:
            user_id = request.form['userId']
            old_user_pronunciation = remove_user_pronunciation(user_id)
            if old_user_pronunciation:
                delete_pronunciation_audio(old_user_pronunciation['audioFileName'])

            return None, 204
        except Exception as e:
            logger.exception("Error occurred while deleting pronunciation")
            return f'Unexpected Error, {str(e)}', 500
