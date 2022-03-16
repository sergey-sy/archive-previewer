from os import sep as os_separator
from typing import Optional
from zipfile import ZipFile, BadZipFile
from logging import getLogger
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from models.queries import is_file_in_files

log = getLogger('console')


class Unpacker(object):
    def __init__(self):
        self.file = None
        self._filename = None
        self._content = list()
        self._restrictions = list()

    def _find_restrictions(self):
        if not self._filename.endswith('.zip'):
            self._restrictions.append('Only *.zip files acceptable')
        if is_file_in_files(self._filename):
            self._restrictions.append("Can't accept the same filename twice")

    def _fill_zip_content(self, zipfile: ZipFile):
        for file_info in zipfile.infolist():
            self._content.append({'path': secure_filename(file_info.filename), 'size': file_info.file_size})
        return

    def _safe_open_zip(self):
        try:
            file_io_bytes = self.file.stream._file
            with ZipFile(file_io_bytes) as zipfile_obj:
                self._fill_zip_content(zipfile_obj)
        except BadZipFile as e:
            log.error(f'BadZipFile exception was caught with message: {e}')
            self._restrictions.append(e)

    def unpack_file(self, file: FileStorage) -> Optional[dict]:
        self.file = file
        self._filename = secure_filename(self.file.filename.split(os_separator)[-1])

        self._find_restrictions()

        if not self._restrictions:
            self._safe_open_zip()
            if not self._restrictions:
                file_content = {
                    'file': self._filename,
                    'content': self._content
                }
                return file_content

    def get_content(self):
        return self._content

    def get_unpacking_errors(self):
        return self._restrictions
