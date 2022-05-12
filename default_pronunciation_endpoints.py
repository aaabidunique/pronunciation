from flask import request, send_file
from flask_restful import Resource

from google_tts_client import generate_and_save_audio
from utils import get_default_audio_file_path, is_default_audio_file_exist


class DefaultPronunciationEndpoints(Resource):
    def get(self):
        if 'userId' not in request.form:
            return "userId missing", 400
        if 'name' not in request.form:
            return "name missing", 400

        # check in bucket if default_userId.mp3 file is present then send as response
        # else create new file default_userId.mp3 using gcp and then as response
        # implement gcp tts
        user_id = request.form['userId']
        name = request.form['name']

        if not is_default_audio_file_exist(user_id):
            try:
                generate_and_save_audio(user_id, name)
            except Exception as e:
                print('Unexpected error', e)
                return "Unexpected Error", 500

        return send_file(
            get_default_audio_file_path(user_id), mimetype="audio/mp3", as_attachment=True,
            download_name=f"default_{user_id}.mp3")
