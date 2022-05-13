from google.cloud import storage


def save_pronunciation_audio_from_string(file_name, source_file_path):
    storage_client = storage.Client()
    bucket = storage_client.bucket('pronunciation')
    blob = bucket.blob(file_name)
    blob.upload_from_string(source_file_path, content_type='audio/mp3')


def save_pronunciation_audio_from_file(file_name, source_file_path):
    storage_client = storage.Client()
    bucket = storage_client.bucket('pronunciation')
    blob = bucket.blob(file_name)
    blob.upload_from_file(source_file_path)


def get_pronunciation_audio(file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket('pronunciation')
    blob = bucket.blob(file_name)
    return blob.download_as_bytes()


def delete_pronunciation_audio(file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket('pronunciation')
    blob = bucket.blob(file_name)
    blob.delete()
