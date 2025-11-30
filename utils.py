import random
import string
import datetime

def generate_cmid() -> str:
    """
    Generates a unique Codiverse Member ID (CMID).
    Format: CMID-YYYYMMDD-XXXX
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"CMID-{timestamp}-{random_chars}"
