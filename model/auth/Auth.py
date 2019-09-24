import asyncio
import html
import os
import aiohttp_jinja2
import aiohttp_session
import jinja2
import ujson
import base64
import uvloop
from aiohttp_session.redis_storage import RedisStorage
from aioredis import create_pool

from cryptography import fernet
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp import web
from pprint import pformat
from aioauth_client import (
    FacebookClient,
    GithubClient,
    GoogleClient,
    OAuth1Client,
    TwitterClient
)

loop = uvloop.new_event_loop()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR.replace("model", ""), 'config_pro.json'), "r") as f:
    json = ujson.loads(f.read())
key = json["key_accept"]
routs = web.RouteTableDef()
app = web.Application()

aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

clients = {
    'twitter': {
        'class': TwitterClient,
        'init': {
            'consumer_key': 'oUXo1M7q1rlsPXm4ER3dWnMt8',
            'consumer_secret': 'YWzEvXZJO9PI6f9w2FtwUJenMvy9SPLrHOvnNkVkc5LdYjKKup',
        },
    },
    'github': {
        'class': GithubClient,
        'init': {
            'client_id': json["github"]["client_id"],
            'client_secret': json["github"]["client_secret"],
        },
    },
    'google': {
        'class': GoogleClient,
        'init': {
            'client_id': '150775235058-9fmas709maee5nn053knv1heov12sh4n.apps.googleusercontent.com',  # noqa
            'client_secret': 'df3JwpfRf8RIBz-9avNW8Gx7',
            'scope': 'email profile',
        },
    },
    'facebook': {
        'class': FacebookClient,
        'init': {
            'client_id': '384739235070641',
            'client_secret': '8e3374a4e1e91a2bd5b830a46208c15a',
            'scope': 'email'
        },
    },
}


@aiohttp_jinja2.template('index.html')
async def index(request):
    print(1)
    context = {}
    session = await get_session(request)
    session["chat_id"] = request.query["chat_id"]
    print(request.query["chat_id"])
    """return aiohttp_jinja2.render_template('index.html',
      request,
        context)"""
    return web.Response(text="""
        <ul>
            <li><a href="/oauth/bitbucket">Login with Bitbucket</a></li>
            <li><a href="/oauth/facebook">Login with Facebook</a></li>
            <li><a href="/oauth/github">Login with Github</a></li>
            <li><a href="/oauth/google">Login with Google</a></li>
            <li><a href="/oauth/twitter">Login with Twitter</a></li>
        </ul>
    """, content_type="text/html")


async def github(request):
    github_auth = GithubClient(
        client_id='b6281b6fe88fa4c313e6',
        client_secret='21ff23d9f1cad775daee6a38d230e1ee05b04f7c',
    )
    if 'code' not in request.query:
        return web.HTTPFound(github_auth.get_authorize_url(scope='user:email'))

    # Get access token
    code = request.query['code']

    token, _ = await github_auth.get_access_token(code)
    assert token

    # Get a resource `https://api.github.com/user`
    response = await github_auth.request('GET', 'user')
    body = await response.read()
    return web.Response(body=body, content_type='application/json')


async def oauth(request):
    provider = request.match_info.get('provider')
    if provider not in clients:
        raise web.HTTPNotFound(reason='Unknown provider')
    session = await get_session(request)
    print(session)

    Client = clients[provider]['class']
    params = clients[provider]['init']
    client = Client(**params)
    client.params['oauth_callback' if issubclass(Client, OAuth1Client) else 'redirect_uri'] = \
        'http://%s%s' % (request.host, request.path)

    # Check if is not redirect from provider
    if client.shared_key not in request.query:

        # For oauth1 we need more work
        if isinstance(client, OAuth1Client):
            token, secret, _ = await client.get_request_token()

            # Dirty save a token_secret
            # Dont do it in production
            request.app.secret = secret
            request.app.token = token

        # Redirect client to provider
        return web.HTTPFound(client.get_authorize_url(access_type='offline'))

    # For oauth1 we need more work
    if isinstance(client, OAuth1Client):
        client.oauth_token_secret = request.app.secret
        client.oauth_token = request.app.token

    _, meta = await client.get_access_token(request.query)
    user, info = await client.user_info()
    text = (
        "<a href='/'>back</a><br/><br/>"
        "<ul>"
        "<li>ID: {u.id}</li>"
        "<li>Username: {u.username}</li>"
        "<li>First, last name: {u.first_name}, {u.last_name}</li>"
        "<li>Gender: {u.gender}</li>"
        "<li>Email: {u.email}</li>"
        "<li>Link: {u.link}</li>"
        "<li>Picture: {u.picture}</li>"
        "<li>Country, city: {u.country}, {u.city}</li>"
        "</ul>"
    ).format(u=user)
    text += "<pre>%s</pre>" % html.escape(pformat(info))
    text += "<pre>%s</pre>" % html.escape(pformat(meta))

    return web.Response(text=text, content_type='text/html')


@routs.get("/api/vue.js")
async def get_vue(request) -> web.FileResponse:
    return web.FileResponse(path="./templates/vue.js")


@routs.get("/api/jquery.js")
async def get_jq(request) -> web.FileResponse:
    return web.FileResponse(path="./templates/jquery.js")


@routs.get("/api/")
async def get_token(request) -> web.json_response:
    if request.query["key"] == key:
        return web.json_response({"12": "asdh"})


app.router.add_route('GET', '/', index)
app.router.add_route('GET', '/oauth/{provider}', oauth)
app.add_routes(routs)


async def setup_session() -> None:
    pool = await create_pool(('localhost', 6379), db=0)
    aiohttp_session.setup(app, RedisStorage(pool))


async def shutdown(app_) -> None:
    await app_.shutdown()
    await app_.cleanup()


asyncio.set_event_loop(loop)
loop.run_until_complete(setup_session())
f = loop.create_server(app.make_handler(), json["web"]["host_api"], json["web"]["port"])
srv = loop.run_until_complete(f)
print('serving on', srv.sockets[0].getsockname())

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    loop.run_until_complete(shutdown(app))
    loop.close()
