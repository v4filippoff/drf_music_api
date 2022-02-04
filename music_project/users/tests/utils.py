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


def add_testserver_prefix_to_avatar_files(serialized_users):
    """
    Добавляет префикс 'http://test_server' к url файла-аватара при ручной сериализации, чтобы он совпадал
    с url файла при извлечении response.data
    """
    prefix = 'http://testserver'
    if not isinstance(serialized_users, list):
        serialized_users = [serialized_users,]
    for user in serialized_users:
        if user['avatar']:
            user['avatar'] = prefix + user['avatar']