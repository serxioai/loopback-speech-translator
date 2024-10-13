from pymongo.collection import Collection

class TranslationRepository:
    def __init__(self, db):
        self.collection: Collection = db['translations']

    def save_translation(self, user_id, session_id, timestamp, language_dict):
        try:
            self.collection.insert_one({
                "user_id": user_id,
                "session_id": session_id,
                "timestamp": timestamp,
                "in": language_dict['source'],
                "out": language_dict['target'],
            })
            return True
        except Exception as e:
            print(f"Failed to save translation: {e}")
            return False

    def get_translation_by_id(self, translation_id):
        try:
            return self.collection.find_one({"_id": translation_id})
        except Exception as e:
            print(f"Failed to retrieve translation: {e}")
            return None

    def update_translation(self, translation_id, update_data):
        try:
            result = self.collection.update_one({"_id": translation_id}, {"$set": update_data})
            return result.modified_count > 0
        except Exception as e:
            print(f"Failed to update translation: {e}")
            return False

    def delete_translation(self, translation_id):
        try:
            result = self.collection.delete_one({"_id": translation_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Failed to delete translation: {e}")
            return False

    def get_translations_by_user(self, user_id):
        try:
            return list(self.collection.find({"user_id": user_id}))
        except Exception as e:
            print(f"Failed to retrieve translations for user: {e}")
            return []
        
    def get_translations_by_user_session(self, user_id, session_id):
        try:
            return list(self.collection.find({
                "user_id": user_id,
                "session_id": session_id
            }))
        except Exception as e:
            print(f"Failed to retrieve translations for user session: {e}")
            return []