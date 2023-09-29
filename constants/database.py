from cryptography.fernet import Fernet


# CONSTANTS FOR DATABASE CONFIG
DB_USER = "root"
KEY = "tuf6dvWrw4AtR_yMaG_EjcwPFp68Ge10w-Ci6HemLiU="
HASHED_PASSWORD = "gAAAAABlFzmhpTFwEg6f78oRSyvR6PSYzjKGR8L8xdv_mzRrtwABnvx1mh6CKebnDEXYapeOKb9A_LH8EFLd_CJniIbM4-co1Q=="
fernet = Fernet(KEY)
DB_PASSWORD = fernet.decrypt(HASHED_PASSWORD).decode()
DB_HOST = "localhost"
DB_NAME = "epicevents"
DB_URL = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
