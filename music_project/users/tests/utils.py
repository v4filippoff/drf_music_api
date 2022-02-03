import os
import shutil


def delete_avatars(*avatars):
    """
    Удаляет медиа-директории с аватарами пользователей
    """
    for avatar in avatars:
        dirname_with_image = os.path.dirname(avatar.path)
        try:
            shutil.rmtree(dirname_with_image)
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