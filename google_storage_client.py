from google.cloud import storage


def save_pronunciation(destination_file_name, source_file):
    storage_client = storage.Client()
    bucket = storage_client.bucket('pronunciation')
    blob = bucket.blob(destination_file_name)
    blob.upload_from_filename(source_file)


def get_pronunciation(file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket('pronunciation')
    blob = bucket.blob(file_name)
    return blob.download_as_bytes()


def delete_pronunciation(file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket('pronunciation')
    blob = bucket.blob(file_name)
    blob.delete()
