# utils/security.py
import hashlib
import base64
from datetime import datetime, timedelta
from collections import defaultdict
import time

# برای Rate Limiting
rate_limit_data = defaultdict(list)

def hash_data(data):
    """هش کردن داده"""
    return hashlib.sha256(str(data).encode()).hexdigest()

def encrypt_phone(phone):
    """رمزنگاری شماره تلفن (ساده)"""
    return base64.b64encode(phone.encode()).decode()

def decrypt_phone(encrypted):
    """رمزگشایی شماره تلفن"""
    return base64.b64decode(encrypted.encode()).decode()

def check_rate_limit(user_id, limit=5, window=60):
    """بررسی محدودیت درخواست"""
    now = time.time()
    user_requests = rate_limit_data[user_id]
    
    # پاک کردن درخواست‌های قدیمی
    user_requests = [t for t in user_requests if now - t < window]
    rate_limit_data[user_id] = user_requests
    
    if len(user_requests) >= limit:
        return False
    
    user_requests.append(now)
    rate_limit_data[user_id] = user_requests
    return True

def validate_phone(phone):
    """اعتبارسنجی شماره تلفن"""
    import re
    return bool(re.match(r'^\+?[0-9]{10,15}$', phone))

def generate_verification_code():
    """تولید کد تایید ۶ رقمی"""
    import random
    return str(random.randint(100000, 999999))
