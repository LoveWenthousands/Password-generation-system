from app import create_app, db
from app.models import User

app = create_app()

# 这可以让你在命令行中更方便地操作数据库和应用
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

if __name__ == '__main__':
    app.run(debug=True)