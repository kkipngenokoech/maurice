"""Owner-initiated Google OAuth from WhatsApp, with a separate loopback callback."""

import base64
import json
import os
from hashlib import sha256
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Lock, Thread
from time import monotonic, sleep
from urllib.parse import parse_qs, urlsplit

from google_auth_oauthlib.flow import Flow
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from oauthlib.oauth2 import OAuth2Error
from requests import RequestException, post

from . import GMAIL_SCOPE, SCOPES, get_hermes_home, save_credentials, token_path

CALLBACK_PATH = "/google/callback"
CALLBACK_PORT = 8766
_PENDING = {}
_LOCK = Lock()
_server = None


def _relay_request(redirect, secret, state, action):
    response = post(
        redirect, json={"state": state, "action": action},
        headers={"Authorization": f"Bearer {secret}"},
        timeout=8, allow_redirects=False,
    )
    if response.status_code not in (200, 204):
        raise RequestException("Google callback relay unavailable")
    return response


def _receive_relay(redirect, secret, state):
    try:
        expires, flow, destination, scopes = _PENDING[state]
        key = sha256(f"maurice-oauth-relay:{secret}".encode()).digest()
        while monotonic() < expires:
            sleep(3)
            try:
                result = _relay_request(redirect, secret, state, "read")
            except RequestException:
                continue
            if result.status_code == 204:
                continue
            if monotonic() >= expires:
                return
            sealed = base64.b64decode(result.content, validate=True)
            payload = AESGCM(key).decrypt(sealed[:12], sealed[12:], state.encode())
            code = json.loads(payload)["code"]
            if code:
                flow.fetch_token(code=code, timeout=15)
                save_credentials(destination, flow.credentials, scopes)
            return
    except (InvalidTag, OAuth2Error, RequestException, ValueError, KeyError, OSError):
        return
    finally:
        with _LOCK:
            _PENDING.pop(state, None)


class Callback(BaseHTTPRequestHandler):
    def log_message(self, *args):
        # Callback query strings contain authorization codes.
        pass

    def do_GET(self):
        url = urlsplit(self.path)
        if url.path != CALLBACK_PATH:
            self.send_error(404)
            return
        query = parse_qs(url.query)
        states = query.get("state", [])
        with _LOCK:
            pending = _PENDING.pop(states[0], None) if len(states) == 1 else None
        status, message = 400, "This link expired or was already used. Start again in WhatsApp."
        if pending is not None and pending[0] > monotonic():
            _, flow, destination, scopes = pending
            codes = query.get("code", [])
            if len(codes) == 1 and "error" not in query:
                try:
                    flow.fetch_token(code=codes[0], timeout=15)
                    save_credentials(destination, flow.credentials, scopes)
                    status, message = 200, "Google account connected. You can return to WhatsApp."
                except FileExistsError:
                    status, message = 409, "That account label is already connected."
                except (OAuth2Error, RequestException, ValueError, OSError):
                    message = "Google sign-in failed. Start again in WhatsApp."
            else:
                message = "Google access was not granted. You can return to WhatsApp."
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Referrer-Policy", "no-referrer")
        self.end_headers()
        self.wfile.write(message.encode())


def _owner_chat(platform, source):
    if platform != "whatsapp_agent_platform" or source is None or source.chat_type != "dm":
        return False
    key = os.environ.get("WHATSAPP_AGENT_PLATFORM_API_KEY")
    if not key:
        return False
    try:
        from hermes_plugins.whatsapp_agent_platform.state import read_creator
    except ImportError:
        return False
    creator = read_creator(get_hermes_home(), key)
    return bool(creator and source.user_id == source.chat_id == creator)


def connect_google(raw_args, *, platform="", source=None):
    if not _owner_chat(platform, source):
        return "Google sign-in is available in the owner's private WhatsApp chat."
    account = raw_args.strip() or "primary"
    try:
        destination = token_path(account)
    except ValueError as error:
        return str(error)
    if destination.exists():
        return f"Google account label {account!r} is already connected."

    redirect = os.environ.get("MAURICE_GOOGLE_REDIRECT_URI", "")
    try:
        url = urlsplit(redirect)
        valid = (url.scheme == "https" and url.hostname and not url.username and not url.password
                 and url.path == CALLBACK_PATH and not url.query and not url.fragment)
    except ValueError:
        valid = False
    if not valid:
        return "Google sign-in needs an HTTPS callback configured on the Mac."

    scopes = SCOPES if account == "primary" else (GMAIL_SCOPE,)
    client = destination.parent / "google-web-client.json"
    try:
        flow = Flow.from_client_secrets_file(str(client), scopes, redirect_uri=redirect,
                                             autogenerate_code_verifier=True)
        if flow.client_type != "web":
            return "WhatsApp sign-in needs a Google Web application OAuth client."
        link, state = flow.authorization_url(access_type="offline", prompt="select_account consent")
    except (OSError, ValueError):
        return "Google sign-in needs the Web OAuth client JSON configured on the Mac."

    global _server
    secret = os.environ.get("MAURICE_GOOGLE_RELAY_SECRET")
    if url.hostname == "maurice.kipngenokoech.com" and not secret:
        return "The Google sign-in relay is not configured yet."
    with _LOCK:
        now = monotonic()
        for expired in [key for key, item in _PENDING.items() if item[0] <= now]:
            del _PENDING[expired]
        if len(_PENDING) >= 16:
            return "Too many sign-in links are pending. Try again in a few minutes."
        if secret:
            try:
                _relay_request(redirect, secret, state, "start")
            except RequestException:
                return "The Google sign-in relay is temporarily unavailable."
        elif _server is None:
            try:
                _server = ThreadingHTTPServer(("127.0.0.1", CALLBACK_PORT), Callback)
            except OSError:
                return "Maurice could not start the Google sign-in callback."
            Thread(target=_server.serve_forever, daemon=True).start()
        _PENDING[state] = (monotonic() + 300, flow, destination, scopes)
        if secret:
            Thread(target=_receive_relay, args=(redirect, secret, state), daemon=True).start()
    return f"Open this link within five minutes and choose the Google account for {account!r}.\n\n{link}"
