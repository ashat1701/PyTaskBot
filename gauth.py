import google_auth_oauthlib.flow


class GoogleAuth:
    def __init__(self, chat_id):
        self.chat_id = chat_id

    def generate_url(self):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            'client_secret.json',
            scopes=['https://www.googleapis.com/auth/calendar.events'])

        flow.redirect_uri = "https://server-for-task-bot.herokuapp.com/login"
        state = str(self.chat_id)
        authorization_url, st = flow.authorization_url(
            access_type='offline',
            state=state,
            include_granted_scopes='true')
        return authorization_url
