# utils/database.py
import json
import os
from datetime import datetime
import uuid

DATA_DIR = "data"

def init_db():
    """ایجاد فایل‌های دیتابیس در صورت نبودن"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    files = ["users.json", "transactions.json", "payments.json", "ads.json"]
    for file in files:
        path = os.path.join(DATA_DIR, file)
        if not os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as f:
                if file == "users.json":
                    json.dump({"users": {}, "stats": {"total": 0}}, f, ensure_ascii=False, indent=2)
                else:
                    json.dump([], f, ensure_ascii=False, indent=2)

def load_data(file_name):
    """بارگذاری دیتا از فایل"""
    path = os.path.join(DATA_DIR, file_name)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(file_name, data):
    """ذخیره دیتا در فایل"""
    path = os.path.join(DATA_DIR, file_name)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def generate_id():
    """تولید شناسه یکتا"""
    return str(uuid.uuid4())[:8].upper()

def get_time():
    """دریافت زمان فعلی"""
    return datetime.now().isoformat()

def get_date():
    """دریافت تاریخ فعلی"""
    return datetime.now().strftime("%Y/%m/%d")
