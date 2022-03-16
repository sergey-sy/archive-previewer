from models.database import Session
from models.zip_file_model import File, Content


def select_files() -> list:
    with Session() as session:
        response = []
        for line in session.query(File).all():
            file_obj = line.as_dict()
            file_obj['content'] = [i.as_dict() for i in session.query(Content).filter(Content.file_id == line.id)]
            response.append(file_obj)
        return response


def insert_file(file_content: dict) -> int:
    with Session() as session:
        file = File(name=file_content['file'])
        session.add(file)
        session.flush()
        for content in file_content['content']:
            session.add(Content(path=content['path'], size=content['size'], file_id=file.id))
        session.commit()
        file_content['id'] = file.id
        return file_content


def is_file_in_files(filename: str):
    return bool(Session().query(File).filter(File.name == filename).first())
