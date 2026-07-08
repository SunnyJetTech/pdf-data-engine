class DocumentRepository:

    def __init__(self, db):
        self.db = db

    def get_user_documents(self, user_id):
        ...

    def get_document(self, document_id, user_id):
        ...

    def delete(self):
        ...

    def create(self):
        ...

    def exists(self):
        ...