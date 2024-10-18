from flask import render_template, request, current_app
from flask_cors import cross_origin
from . import avatar_bp
from .parse_friends import parse_friends
from at_client import at_client_extension
from .utils import plot_avatars_full_circle

@avatar_bp.route('/')
def index():
    return render_template('index.html')

@cross_origin()
@avatar_bp.route('/generate', methods=['POST'])
def generate_avatar():
    client = at_client_extension.get_client()

    handle = request.form.get('handle')
    # filter invisible characters
    handle = ''.join(filter(lambda x: x.isprintable(), handle))
    handle.replace('@', '')
    friends_data = parse_friends(client, handle)
    center = client.get_profile(handle)
    center_avatar_url = center.avatar
    data = plot_avatars_full_circle(friends_data, center_avatar_url)
    res = current_app.make_response(data)
    res.headers['Content-Type'] = 'image/png'
    return res