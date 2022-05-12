import os


def get_audio_file_path(user_id: str):
    return os.path.join(os.getcwd(), f'recordings/{user_id}.mp3')


def get_default_audio_file_path(user_id: str):
    return os.path.join(os.getcwd(), f'recordings/default_{user_id}.mp3')


def is_default_audio_file_exist(user_id: str):
    return os.path.exists(get_default_audio_file_path(user_id))
