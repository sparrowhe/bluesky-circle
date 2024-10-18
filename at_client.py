from flask import current_app
from atproto import Client
class ATProtoClientExtension:
    def __init__(self):
        self.client_instance = None

    def init_app(self, app):
        app.before_request(self.before_request)
        app.extensions['at_client'] = self

    def before_request(self):
        if self.client_instance is None:
            self.client_instance = Client(base_url=current_app.config['BLUESKY_BASE'])
            self.client_instance.login(current_app.config['BLUESKY_HANDLE'], current_app.config['BLUESKY_PASSWORD'])

    def get_client(self):
        return self.client_instance

at_client_extension = ATProtoClientExtension()
