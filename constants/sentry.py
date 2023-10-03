from cryptography.fernet import Fernet
import dotenv, os
dotenv.load_dotenv()


# CONSTANTS FOR SENTRY CONFIG
hashed_data1 = "gAAAAABlF0AbFlQx0cXhkCLJwZCT_HgGMJPG9xqZxEIPZmvwvEBN3LRO6M87a8e0UoxrNeamjlJReOOkAqAK69sKyqIZsQpjq8E9tEmXu1x2PqTPsFYtUYVe-LG7yvGfLt7A5m_JhF-dzYgngnXqj8zMO1Y7BXgj2Q=="
hashed_data2 = "gAAAAABlFz_91yDYOZ3mxAj7neDBiZNjnWGqoh907OX2glS39PFRnycvmasqfXBKFb7c8jy7-i7KIP8ZWPMFBxduWvwCwbc3NKrmVaCBx_rV1S_Bu45PMHA="
fernet1 = Fernet(os.getenv("key1_sentry"))
fernet2 = Fernet(os.getenv("key2_sentry"))
data1 = fernet1.decrypt(hashed_data1).decode()
data2 = fernet2.decrypt(hashed_data2).decode()
DSN = f"https://{data1}.ingest.sentry.io/{data2}"