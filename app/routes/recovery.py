import json
from flask import render_template, request, flash, redirect, url_for
from flask.blueprints import Blueprint
from flask_login import login_required, current_user
from app import db
from app.services.llm_service import get_embedding_from_llm
from app.services.crypto_service import calculate_similarity, serialize_vector, deserialize_vector

bp = Blueprint('recovery', __name__)

# --- 注册秘密的路由 ---
@bp.route('/register-secret', methods=['GET', 'POST'])
@login_required
def register_secret():
    if request.method == 'POST':
        secret_text = request.form.get('secret_text', '').strip()
        if len(secret_text) < 20:
            flash('为了安全，秘密描述长度不能少于20个字。')
        else:
            # 1. 获取文本的向量
            vector = get_embedding_from_llm(secret_text)
            if vector:
                # 2. 将向量序列化为字符串
                vector_json = serialize_vector(vector)
                # 3. 存入当前用户的数据库记录中
                current_user.secret_vector = vector_json
                db.session.commit()
                flash('您的语义密钥已成功设置！')
                return redirect(url_for('index'))
            else:
                flash('无法生成语义密钥，请稍后再试。')
                
    return render_template('register_secret.html', title='设置语义密钥')

# --- 恢复账户的路由 ---
@bp.route('/recover', methods=['GET', 'POST'])
def recover():
    if not current_user.is_authenticated or not current_user.secret_vector:
         flash('请先登录并设置语义密钥，才能进行恢复测试。')
         return redirect(url_for('auth.login'))

    if request.method == 'POST':
        answer_text = request.form.get('answer_text', '').strip()
        if not answer_text:
            flash('请输入您的描述。')
        else:
            # 1. 从数据库取出存储的秘密向量字符串并反序列化
            stored_vector = deserialize_vector(current_user.secret_vector)
            
            stored_vector = deserialize_vector(current_user.secret_vector)
            
            # 2. 获取用户当前回答的向量
            answer_vector = get_embedding_from_llm(answer_text)
            
            if answer_vector is None:
                flash('无法处理您的描述，请稍后再试。')
                return render_template('recovery.html', title='重置主密码')
            
            # 3. 计算相似度
            similarity = calculate_similarity(stored_vector, answer_vector)
            
            # 4. 根据阈值判断
            SIMILARITY_THRESHOLD = 0.8  # 这是一个经验阈值
            
            if similarity >= SIMILARITY_THRESHOLD:
                # 验证通过，允许重置主密码
                flash(f'验证成功！语义相似度: {similarity:.4f}')
                return redirect(url_for('recovery.reset_password'))
            else:
                flash(f'验证失败。语义相似度: {similarity:.4f}，未达到阈值 {SIMILARITY_THRESHOLD}。请重试。')

    return render_template('recovery.html', title='重置主密码')

@bp.route('/reset-password', methods=['GET', 'POST'])
@login_required
def reset_password():
    """重置主密码的路由"""
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not new_password or not confirm_password:
            flash('请填写所有密码字段。')
            return render_template('reset_password.html', title='重置主密码')
            
        if new_password != confirm_password:
            flash('两次输入的密码不匹配。')
            return render_template('reset_password.html', title='重置主密码')
            
        # 更新用户的主密码
        current_user.set_password(new_password)
        db.session.commit()
        
        flash('主密码已成功重置！请使用新密码登录。')
        return redirect(url_for('auth.login'))
        
    return render_template('reset_password.html', title='重置主密码')
