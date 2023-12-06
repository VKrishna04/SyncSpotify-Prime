# primemusic_auth.py
from spotipy.oauth2 import SpotifyOAuth

PRIME_SCOPE = "your_prime_scopes"


class PrimeMusicAuthenticator:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.sp_oauth = SpotifyOAuth(
            client_id, client_secret, redirect_uri, scope=PRIME_SCOPE
        )

    def get_authorization_url(self):
        return self.sp_oauth.get_authorize_url()

    def get_access_token(self, redirect_url):
        code = self.sp_oauth.parse_response_code(redirect_url)
        if code:
            token_info = self.sp_oauth.get_access_token(code)
            return token_info
        return None
