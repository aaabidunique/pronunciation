from pathlib import Path

from pysondb import db

db_directory = Path('db')
db_directory.mkdir(exist_ok=True)

recordings_directory = Path('recordings')
recordings_directory.mkdir(exist_ok=True)

user_pronunciation_db = db.getDb("db/tbl_user_pronunciation.json")
user_pronunciation_audio_settings_db = db.getDb("db/tbl_user_pronunciation_audio_settings.json")


def get_user_pronunciation(user_id: str):
    pronunciation = user_pronunciation_db.getByQuery({'userId': user_id})
    if not pronunciation:
        return dict()
    else:
        return pronunciation[0]


def save_user_pronunciation(user_id: str, legal_first_name: str, legal_last_name: str, preferred_name: str,
                            audio_file_name: str):
    saved_pronunciation = get_user_pronunciation(user_id)
    if not saved_pronunciation:
        user_pronunciation_db.add(
            {'userId': user_id, 'legalFirstName': legal_first_name, 'legalLastName': legal_last_name,
             'preferredName': preferred_name, 'audioFileName': audio_file_name})
    else:
        user_pronunciation_db.updateById(saved_pronunciation['id'],
                                         {'userId': user_id, 'legalFirstName': legal_first_name,
                                          'legalLastName': legal_last_name,
                                          'preferredName': preferred_name, 'audioFileName': audio_file_name})
    return saved_pronunciation


def remove_user_pronunciation(user_id: str):
    saved_pronunciation = get_user_pronunciation(user_id)
    if saved_pronunciation:
        user_pronunciation_db.deleteById(saved_pronunciation['id'])
    return saved_pronunciation
