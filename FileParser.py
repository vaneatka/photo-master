import hashlib
import sqlite3
import os

class FileParser:

    sql_create_images_table = """ CREATE TABLE IF NOT EXISTS images (
    id           integer      not null  primary key AUTOINCREMENT UNIQUE,
    path         varchar(255) not null,
    size         integer      not null,
    hash         varchar(255) not null,
    date_created timestamp(0) not null,
    extension    text         not null,
    CONSTRAINT UNIQUE_PATH UNIQUE (path,hash)
); """

    def db_connection(self):
        connection = sqlite3.connect('./db/database.sqlite', isolation_level=None)
        cursor = connection.cursor()
        cursor.execute(self.sql_create_images_table)
        return connection

    def sha256sum(self, filename):
        h = hashlib.sha256()
        b = bytearray(128 * 1024)
        mv = memoryview(b)
        with open(filename, 'rb', buffering=0) as f:
            for n in iter(lambda: f.readinto(mv), 0):
                h.update(mv[:n])
        return h.hexdigest()

    def saveImageInfo(self):
        conn = self.db_connection()


    def save_image(self, image):
        conn = self.db_connection()
        cursor = conn.cursor()
        try:
            [image, file_hash, file_size, date_created, file_extension] = self.get_image_info(image)
            result = cursor.execute("""
                INSERT OR IGNORE INTO images (
                path,
                size,
                hash,
                date_created,
                extension ) VALUES (?,?,?,?,?)
            """, (
                 image,
                 file_size,
                 file_hash,
                 date_created,
                 file_extension,
            )).fetchone()
            print((
                 image,
                 file_hash,
                 file_size,
                 date_created,
                 file_extension,
            ))
        except ValueError:
            print(ValueError)

    def get_image_info(self, image):
        file_object = os.stat(image)
        file_hash = self.sha256sum(image)
        file_size = file_object.st_size
        date_created = file_object.st_mtime
        filename, file_extension = os.path.splitext(image)
        return [image, file_hash, file_size, date_created, file_extension]

    def isImage(self, extension):
        return extension.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))





