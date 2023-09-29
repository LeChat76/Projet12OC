from cryptography.fernet import Fernet


# CONSTANTS FOR SENTRY CONFIG
KEY1 = "vnKejgnhlbaEbONON14CZAnyr5aTfj0bXzkzLFhp80I="
KEY2 = "4_uGlqAjY385qvbOTHcWaPafqewxNczzz-cCW4ngj1I="
HASHED_DATA1 = "gAAAAABlF0AbFlQx0cXhkCLJwZCT_HgGMJPG9xqZxEIPZmvwvEBN3LRO6M87a8e0UoxrNeamjlJReOOkAqAK69sKyqIZsQpjq8E9tEmXu1x2PqTPsFYtUYVe-LG7yvGfLt7A5m_JhF-dzYgngnXqj8zMO1Y7BXgj2Q=="
HASHED_DATA2 = "gAAAAABlFz_91yDYOZ3mxAj7neDBiZNjnWGqoh907OX2glS39PFRnycvmasqfXBKFb7c8jy7-i7KIP8ZWPMFBxduWvwCwbc3NKrmVaCBx_rV1S_Bu45PMHA="
fernet1 = Fernet(KEY1)
fernet2 = Fernet(KEY2)
DATA1 = fernet1.decrypt(HASHED_DATA1).decode()
DATA2 = fernet2.decrypt(HASHED_DATA2).decode()
DSN = f"https://{DATA1}.ingest.sentry.io/{DATA2}"