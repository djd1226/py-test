import os

class Config:
    DATA_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'data.json')
    SECRET_KEY = 'your_secret_key'  # 用于表单的CSRF保护
