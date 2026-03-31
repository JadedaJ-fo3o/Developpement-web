from flask import Blueprint, render_template
from routes.auth import login_required

listeseries_bp = Blueprint('listeseries', __name__)


@listeseries_bp.route('/listeseries')
@login_required
def listeseries_test():
	return render_template('listeseries.html')
