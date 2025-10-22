from flask import render_template, request, flash
from flask.blueprints import Blueprint
from flask_login import login_required
from app.services.llm_service import generate_passphrase_from_llm
from app.services.crypto_service import hash_passphrase

bp = Blueprint('generation', __name__)

@bp.route('/generate', methods=['GET', 'POST'])
@login_required # 确保用户必须登录才能访问这个页面
def generate():
    if request.method == 'POST':
        keywords_str = request.form.get('keywords', '')
        keywords  = [k.strip() for k in keywords_str.split(',') if k.strip()]
       
        if not keywords:
            flash('请输入至少一个关键词。')
            return render_template('generation.html', title='生成密码')
            
        # 调用AI服务生成密码短语
        passphrase = generate_passphrase_from_llm(keywords)
        
        # 对短语进行哈希（注意：实际项目中，这个哈希值应该与用户账户关联并存储，这里只做演示）
        hashed_passphrase = hash_passphrase(passphrase)
        
        return render_template('generation.html', title='生成密码', passphrase=passphrase, hashed_passphrase=hashed_passphrase)
        
    return render_template('generation.html', title='生成密码')