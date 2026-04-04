from flask import Blueprint, jsonify, request, redirect, url_for, make_response, session


shared_bp = Blueprint('shared', __name__)


"""
++++++++++++++++++
==================
    SHARED       |
==================
++++++++++++++++++
"""    


@shared_bp.route('/api/logout', methods=['GET'])
def logout():
    session.clear()
    redirect_url = url_for('front.home')
    response = make_response()
    response.headers['HX-Redirect'] = redirect_url
    return response
