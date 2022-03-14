from typing import Union, Optional
from zipfile import ZipFile
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from models.queries import is_file_in_files


def _find_restrictions(filename) -> Optional[tuple]:
    if is_file_in_files(filename):
        return "Can't accept the same filename twice", 400
    if not filename.endswith('.zip'):
        return "Only *.zip files acceptable", 415


def get_zip_content(zipfile: ZipFile) -> []:
    content = []
    for file_info in zipfile.infolist():
        content.append({'path': secure_filename(file_info.filename), 'size': file_info.file_size})
    return content


def unpack_file(file: FileStorage) -> Union[dict, tuple]:
    filename = secure_filename(file.filename.split('/')[-1])
    restrictions = _find_restrictions(filename)

    if not restrictions:
        file_io_bytes = file.stream._file
        zipfile_obj = ZipFile(file_io_bytes)
        content = get_zip_content(zipfile_obj)
        file_content = {
            'file': filename,
            'content': content
        }
        return file_content
    else:
        return restrictions
