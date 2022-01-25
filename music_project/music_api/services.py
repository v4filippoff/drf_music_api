def get_track_cover_upload_path(instance, filename):
    """
    Возвращает путь в файловой системе для сохранения обложки трека
    Формат: {MEDIA_ROOT}/track_covers/user_{user_id}/{filename}
    """
    return 'track_covers/user_{0}/{1}'.format(instance.id, filename)


def get_album_cover_upload_path(instance, filename):
    """
    Возвращает путь в файловой системе для сохранения обложки альбома
    Формат: {MEDIA_ROOT}/album_covers/user_{user_id}/{filename}
    """
    return 'album_covers/user_{0}/{1}'.format(instance.id, filename)


def get_track_upload_path(instance, filename):
    """
        Возвращает путь в файловой системе для сохранения трека
        Формат: {MEDIA_ROOT}/tracks/user_{user_id}/{filename}
        """
    return 'tracks/user_{0}/{1}'.format(instance.id, filename)