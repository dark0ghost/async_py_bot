from aioauth_client import GithubClient, GoogleClient


class Auth:
    def __init__(self, github_client_id: str, github_client_secret: str, mail: str, nickname: str) -> None:
        self.redirect_uri = ""
        self.github: GithubClient = GithubClient(
            client_id=github_client_id,
            client_secret=github_client_secret,
        )
        self.google: GoogleClient
        self.secret_key = b""
        self.nick: str = nickname
        self.mail: str = mail

    def Github(self):
        authorize_url = self.github.get_authorize_url(scope=f"{self.nick}:{self.email}")
        return authorize_url

    def google(self):
        return
