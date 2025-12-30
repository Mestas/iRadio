import json
import hashlib
import os
from datetime import datetime

# 用户配置文件路径
USER_CONFIG_FILE = 'user_config.json'

# 默认用户配置
DEFAULT_USERS = {
    'cyan': {
        'password_hash': 'bad7b8eaa691b49fcc555cd5e0c09d81257728a7e2a05a86fd2884a8e374ddfa',
        'created_at': datetime.now().isoformat(),
        'last_login': None,
        'is_active': True,
        'role': 'admin'
    }
}

def init_user_config():
    """初始化用户配置文件"""
    if not os.path.exists(USER_CONFIG_FILE):
        save_user_config(DEFAULT_USERS)
        return DEFAULT_USERS
    return load_user_config()

def load_user_config():
    """加载用户配置"""
    try:
        with open(USER_CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载用户配置失败: {e}")
        return DEFAULT_USERS

def save_user_config(users_config):
    """保存用户配置"""
    try:
        with open(USER_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(users_config, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存用户配置失败: {e}")
        return False

def hash_password(password):
    """计算密码的SHA-256哈希值"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(username, password):
    """验证用户名和密码"""
    users = load_user_config()
    if username in users and users[username]['is_active']:
        return users[username]['password_hash'] == hash_password(password)
    return False

def update_user_password(username, new_password):
    """更新用户密码"""
    users = load_user_config()
    if username in users:
        users[username]['password_hash'] = hash_password(new_password)
        users[username]['last_password_change'] = datetime.now().isoformat()
        return save_user_config(users)
    return False

def get_user_info(username):
    """获取用户信息"""
    users = load_user_config()
    if username in users:
        user_info = users[username].copy()
        # 不返回密码哈希值
        user_info.pop('password_hash', None)
        return user_info
    return None

def update_last_login(username):
    """更新用户最后登录时间"""
    users = load_user_config()
    if username in users:
        users[username]['last_login'] = datetime.now().isoformat()
        save_user_config(users)
