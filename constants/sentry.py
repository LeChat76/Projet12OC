from cryptography.fernet import Fernet


# CONSTANTS FOR SENTRY CONFIG
key1 = "vnKejgnhlbaEbONON14CZAnyr5aTfj0bXzkzLFhp80I="
key2 = "4_uGlqAjY385qvbOTHcWaPafqewxNczzz-cCW4ngj1I="
hashed_data1 = "gAAAAABlF0AbFlQx0cXhkCLJwZCT_HgGMJPG9xqZxEIPZmvwvEBN3LRO6M87a8e0UoxrNeamjlJReOOkAqAK69sKyqIZsQpjq8E9tEmXu1x2PqTPsFYtUYVe-LG7yvGfLt7A5m_JhF-dzYgngnXqj8zMO1Y7BXgj2Q=="
hashed_data2 = "gAAAAABlFz_91yDYOZ3mxAj7neDBiZNjnWGqoh907OX2glS39PFRnycvmasqfXBKFb7c8jy7-i7KIP8ZWPMFBxduWvwCwbc3NKrmVaCBx_rV1S_Bu45PMHA="
fernet1 = Fernet(key1)
fernet2 = Fernet(key2)
data1 = fernet1.decrypt(hashed_data1).decode()
data2 = fernet2.decrypt(hashed_data2).decode()
DSN = f"https://{data1}.ingest.sentry.io/{data2}"