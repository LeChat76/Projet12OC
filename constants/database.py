from cryptography.fernet import Fernet


# CONSTANTS FOR DATABASE CONFIG
KEY1 = "tuf6dvWrw4AtR_yMaG_EjcwPFp68Ge10w-Ci6HemLiU="
KEY2 = "mSB7nzr98DSOZWN-_UNTui_DGAriMjvap4R_udyqvVk="
hashed_data1 = "gAAAAABlFzmhpTFwEg6f78oRSyvR6PSYzjKGR8L8xdv_mzRrtwABnvx1mh6CKebnDEXYapeOKb9A_LH8EFLd_CJniIbM4-co1Q=="
hashed_data2 = "gAAAAABlF0c4AtDo0e_o9k8IC62SxtitSOX5WAMXI61CybyzD7BaxcwMRT4s5SSNWZ-ixSQKobZgVR-7u-Mri0fzLNw25T_tpw=="
fernet1 = Fernet(KEY1)
fernet2 = Fernet(KEY2)
db_user = fernet2.decrypt(hashed_data2).decode()
db_password = fernet1.decrypt(hashed_data1).decode()
db_host = "localhost"
db_name = "epicevents"
DB_URL = f"mysql://{db_user}:{db_password}@{db_host}/{db_name}"
