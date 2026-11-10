"""Connect one Google account with desktop OAuth and a loopback callback."""

import argparse

from google_auth_oauthlib.flow import InstalledAppFlow

from __init__ import GMAIL_SCOPE, SCOPES, save_credentials, token_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("client_json", help="Downloaded Google Desktop app OAuth client JSON")
    parser.add_argument("--account", default="primary",
                        help="Account label. Primary connects Calendar and Gmail. Other labels connect Gmail only.")
    args = parser.parse_args()
    try:
        destination = token_path(args.account)
    except ValueError as error:
        parser.error(str(error))
    if destination.exists():
        parser.error(f"Account label {args.account!r} is already connected.")

    scopes = SCOPES if args.account == "primary" else (GMAIL_SCOPE,)
    flow = InstalledAppFlow.from_client_secrets_file(args.client_json, scopes, autogenerate_code_verifier=True)
    credentials = flow.run_local_server(host="127.0.0.1", port=0, open_browser=False,
                                        timeout_seconds=300, prompt="select_account consent")
    try:
        save_credentials(destination, credentials, scopes)
    except (ValueError, FileExistsError) as error:
        parser.error(str(error))
    print(f"Google account {args.account!r} connected.")


if __name__ == "__main__":
    main()
