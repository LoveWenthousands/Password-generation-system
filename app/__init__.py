from flask import Flask,render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager,current_user


# 初始化各个插件
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login' # 如果用户没登录就访问需要登录的页面，会跳转到这里

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # 注册用户认证蓝图
    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # 【新代码】注册我们的新功能蓝图
    from app.routes.generation import bp as generation_bp
    app.register_blueprint(generation_bp)

    from app.routes.recovery import bp as recovery_bp
    app.register_blueprint(recovery_bp)

    # 【修改】修改首页路由，让它显示一个真正的首页
    @app.route('/')
    def index():
        return render_template('index.html', title='首页')

    return app