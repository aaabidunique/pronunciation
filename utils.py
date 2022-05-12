import os


def generate_audio_file_path(file_name: str):
    return os.path.join(os.getcwd(), 'recordings', f'{file_name}.mp3')
