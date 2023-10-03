from cryptography.fernet import Fernet
import dotenv, os
dotenv.load_dotenv()


# CONSTANTS FOR DATABASE CONFIG
hashed_data1_admin = "gAAAAABlHBmMLaE90CQTeGxAf6ItcLRtTs2A_qe_cH9-LMCUXCkHkYRE9nCifINdv0DMPD-mMa1j9t7euj4ZwLa4G4rSuoqNsydLHfU8ZowAEkB67oHwDJk="
hashed_data2_admin = "gAAAAABlHBFkRllIGTN2WCFqg5wzddXi59xW9a53D7Q8A4nbWg76S57HD7nbT9TKACkqsPiyUd6xKElunwH-_NoMrJX2VbL4Kw=="
hashed_data1_guest = "gAAAAABlHBmoHwcSpKPNOM3yV5i0j9iETxiQ4SZAz888v77Q8o0szGutvFrWjTPFE3Pgg8wWu6_w0FMnyU4H0DO2JM7mdLzNfPAK0g8fyiAuVrWGGe7RR0w="
hashed_data2_guest = "gAAAAABlHBGKQpB_8XpQwTt1jBUs1Uq-7Gz4A-APO6unggpflSzcjIPBpXlb94SMxz8M637Mq-N5jsPcRCL2SWgcuVh8ip_bpQ=="
fernet1_admin = Fernet(os.getenv("key1_admin_database"))
fernet2_admin = Fernet(os.getenv("key2_admin_database"))
fernet1_guest = Fernet(os.getenv("key1_guest_database"))
fernet2_guest = Fernet(os.getenv("key2_guest_database"))
db_user_admin = fernet1_admin.decrypt(hashed_data1_admin).decode()
db_password_admin = fernet2_admin.decrypt(hashed_data2_admin).decode()
db_user_guest = fernet1_guest.decrypt(hashed_data1_guest).decode()
db_password_guest = fernet2_guest.decrypt(hashed_data2_guest).decode()
db_host = "localhost"
db_name = "epicevents"
DB_URL_ADMIN = f"mysql://{db_user_admin}:{db_password_admin}@{db_host}/{db_name}"
DB_URL_GUEST = f"mysql://{db_user_guest}:{db_password_guest}@{db_host}/{db_name}"
