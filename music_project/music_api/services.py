def get_track_cover_upload_path(instance, filename):
    """
    Возвращает путь в файловой системе для сохранения обложки трека
    Формат: {MEDIA_ROOT}/track_covers/track_{track_id}/{filename}
    """
    return 'track_covers/track_{0}/{1}'.format(instance.id, filename)


def get_album_cover_upload_path(instance, filename):
    """
    Возвращает путь в файловой системе для сохранения обложки альбома
    Формат: {MEDIA_ROOT}/album_covers/album_{album_id}/{filename}
    """
    return 'album_covers/album_{0}/{1}'.format(instance.id, filename)


def get_track_upload_path(instance, filename):
    """
        Возвращает путь в файловой системе для сохранения трека
        Формат: {MEDIA_ROOT}/tracks/track_{track_id}/{filename}
        """
    return 'tracks/track_{0}/{1}'.format(instance.id, filename)