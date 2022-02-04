import shutil

from django.conf import settings


def remove_test_media_dir():
    """
    Удаляет тестовую медиа-директорию
    """
    try:
        shutil.rmtree(settings.TEST_MEDIA_ROOT)
    except FileNotFoundError:
        pass


def add_testserver_prefix_to_track_files(serialized_tracks):
    """
    Добавляет префикс 'http://test_server' к url файла-трека при ручной сериализации, чтобы он совпадал
    с url файла при извлечении response.data
    """
    prefix = 'http://testserver'
    if not isinstance(serialized_tracks, list):
        serialized_tracks = [serialized_tracks,]
    for track in serialized_tracks:
        track['file'] = prefix + track['file']