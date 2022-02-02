import os
import shutil


def delete_tracks(*track_files):
    """
    Удаляет медиа-директории с треками
    """
    for file in track_files:
        dirname_with_track = os.path.dirname(file.path)
        try:
            shutil.rmtree(dirname_with_track)
        except FileNotFoundError:
            pass


def add_testserver_prefix_to_track_files(serialized_tracks):
    """
    Добавляет префикс 'http://test_server' к url файла-трека при ручной сериализации, чтобы он совпадал
    с url файла при извлечении response.data
    """
    prefix = 'http://testserver'
    for track in serialized_tracks:
        track['file'] = prefix + track['file']