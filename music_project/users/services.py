def get_avatar_upload_path(instance, filename):
    """
    Возвращает путь в файловой системе для сохранения аватара пользователя
    Формат: {MEDIA_ROOT}/avatars/user_{user_id}/{filename}
    """
    return 'avatars/user_{0}/{1}'.format(instance.id, filename)