import os
import errno


def ensure_folder(path):
    """
    Makes sure that a folder exists. If it doesn't, it creates it.

    :param path: folder to be ensured.
    """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise