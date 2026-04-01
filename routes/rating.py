from flask import Blueprint, render_template
from routes.auth import login_required

rating_bp = Blueprint('rating', __name__)


@rating_bp.route('/rating')
@login_required
def rating_test():
    return render_template('detaille.html')


@rating_bp.route('/detaille')
@login_required
def detaille_test():
    return render_template('detaille.html')

