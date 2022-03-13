from typing import Optional
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import zipfile


def unpack_file(file: FileStorage) -> Optional[dict]:
    filename = secure_filename(file.filename)
    if filename.endswith('.zip'):
        file_io_bytes = file.stream._file
        zipfile_ob = zipfile.ZipFile(file_io_bytes)
        content = []
        for file_info in zipfile_ob.infolist():
            content.append({'path': secure_filename(file_info.filename), 'size': file_info.file_size})
        file_content = {
            'file': filename,
            'content': content
        }
        return file_content
