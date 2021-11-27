import SPDatabase
import SPSecurity


def __loader() -> SPDatabase.DataManager:
    """
    :exception FILE_SUPPORT_ERROR
    :exception SPCrypto.FILE_SUPPORT_ERROR
    :exception SPCrypto.PERMISSION_ERROR
    :exception pickle.UnpicklingError
    :exception MemoryError, PermissionError
    :return: SPDatabase.DataManager
    """

    # Memory setup
    config = SPDatabase.FileConfig(backup=True)
    config.database_update(file='database')
    config.backup_update(file='payroma', extension='backup')
    config.setup()

    # Default configuration and load
    database = SPDatabase.DataManager(
        config, SPSecurity.secure_string(
            # Set the application password here, EX: test = (116, 101, 115, 116)
            (116, 101, 115, 116)
        ).decode()
    )
    database.load()

    # Upgrade to database V2
    # upgrade_to_v2(database.get_data())

    return database


db = __loader()
