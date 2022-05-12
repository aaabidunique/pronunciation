from pysondb import db

user_pronunciation_db = db.getDb("db/tbl_user_pronunciation.json")
user_pronunciation_audio_settings_db = db.getDb("db/tbl_user_pronunciation_audio_settings.json")


def get_user_pronunciation(user_id: str):
    pronunciation = user_pronunciation_db.getByQuery({'userId': user_id})
    if not pronunciation:
        return dict()
    else:
        return pronunciation[0]


def save_user_pronunciation(user_id: str, name: str):
    saved_pronunciation = get_user_pronunciation(user_id)
    if not saved_pronunciation:
        user_pronunciation_db.add({'userId': user_id, 'name': name})
    else:
        user_pronunciation_db.updateById(saved_pronunciation['id'], {'userId': user_id, 'name': name})


def remove_user_pronunciation(user_id: str):
    saved_pronunciation = get_user_pronunciation(user_id)
    if saved_pronunciation:
        user_pronunciation_db.deleteById(saved_pronunciation['id'])
