from flask import render_template
from flask_login import login_required, current_user
from app.user_dashboard import bp

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('user_dashboard/user_dashboard.html', title='Dashboard') 