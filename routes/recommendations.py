from flask import Blueprint, render_template
from routes.auth import login_required

recommendations_bp = Blueprint('recommendations', __name__)


@recommendations_bp.route('/recommendations')
@login_required
def recommendation_test():
	return render_template('recommendations.html')
