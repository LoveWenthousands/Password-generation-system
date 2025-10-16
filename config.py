import os
from dotenv import load_dotenv

# 加载.env文件中的环境变量
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # 从.env文件中读取密钥，如果找不到就用后面的默认值
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # 配置数据库路径，这里我们使用简单的SQLite数据库
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False