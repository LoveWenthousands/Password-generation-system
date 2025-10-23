from flask import render_template, request, flash, redirect, url_for, jsonify
from flask.blueprints import Blueprint
from flask_login import login_required, current_user
from app.services.password_service import generate_random_password, encrypt_password, decrypt_password
from app.models import StoredPassword, User
from app import db

bp = Blueprint('generation', __name__)

@bp.route('/passwords', methods=['GET'])
@login_required
def list_passwords():
    """显示用户保存的所有服务密码"""
    stored_passwords = current_user.stored_passwords.all()
    return render_template('password_list.html', title='我的密码', passwords=stored_passwords)

@bp.route('/generate', methods=['GET', 'POST'])
@login_required
def generate():
    if request.method == 'POST':
        service_name = request.form.get('service_name', '').strip()
        password_length = int(request.form.get('length', '16'))
        
        if not service_name:
            flash('请输入服务名称。')
            return render_template('generation.html', title='生成密码')
        
        # 生成随机密码
        password = generate_random_password(password_length)
        
        # 如果点击了"保存"按钮
        if 'save' in request.form:
            # 使用主密码（用户当前的登录密码）加密服务密码
            encrypted_pass, salt = encrypt_password(password, request.form['current_password'])
            
            # 创建新的存储密码记录
            stored_password = StoredPassword(
                owner=current_user,
                service_name=service_name,
                encrypted_password=encrypted_pass,
                salt=salt
            )
            
            db.session.add(stored_password)
            db.session.commit()
            
            flash(f'密码已为服务 {service_name} 生成并安全保存！')
            return redirect(url_for('generation.list_passwords'))
            
        # 如果只是生成但不保存
        return render_template('generation.html', title='生成密码', 
                             password=password, service_name=service_name)
        
    return render_template('generation.html', title='生成密码')

@bp.route('/passwords/<int:id>/show', methods=['POST'])
@login_required
def show_password(id):
    """显示特定服务的密码"""
    stored_password = StoredPassword.query.get_or_404(id)
    
    # 确保只能查看自己的密码
    if stored_password.user_id != current_user.id:
        return jsonify({
            'success': False,
            'message': '未授权的访问'
        }), 403
    
    # 验证主密码
    current_password = request.form.get('current_password')
    if not current_password:
        return jsonify({
            'success': False,
            'message': '请输入主密码'
        }), 400
    
    if not current_user.check_password(current_password):
        return jsonify({
            'success': False,
            'message': '主密码错误'
        }), 400
    
    try:
        # 解密密码
        decrypted_password = decrypt_password(
            stored_password.encrypted_password,
            current_password,
            stored_password.salt
        )
        return jsonify({
            'success': True,
            'password': decrypted_password,
            'service_name': stored_password.service_name
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': '密码解密失败'
        }), 500

@bp.route('/passwords/<int:id>/delete', methods=['POST'])
@login_required
def delete_password(id):
    """删除保存的密码"""
    stored_password = StoredPassword.query.get_or_404(id)
    
    # 确保只能删除自己的密码
    if stored_password.user_id != current_user.id:
        flash('未授权的访问')
        return redirect(url_for('generation.list_passwords'))
    
    db.session.delete(stored_password)
    db.session.commit()
    flash(f'已删除 {stored_password.service_name} 的密码')
    return redirect(url_for('generation.list_passwords'))
