import sys
from PyQt5.QtWidgets import QApplication, QInputDialog
from spotify_auth import SpotifyAuthenticator
from SyncSpotify_Prime import SyncSpotify_Prime
from primemusic_auth import (
    PrimeMusicAuthenticator,
)  # These do not exist yet
from SyncPrimeMusic import SyncPrimeMusic  # These do not exist yet
from flask import Flask, redirect, request, render_template, jsonify
from flask_executor import Executor
from SyncSpotify_Prime import SyncSpotify_Prime
from sync_logic import (
    sync_spotify_to_spotify,
    sync_spotify_to_prime,
    sync_prime_to_spotify,
    sync_prime_to_prime,
)


# Initialize the Flask app
flask_app = Flask(__name__, template_folder="templates")
flask_app.config["EXECUTOR_TYPE"] = "thread"
flask_app.config["EXECUTOR_MAX_WORKERS"] = 2  # Adjust as needed
executor = Executor(flask_app)


class AppContext:
    spotify_accounts = []  # List to store Spotify access tokens
    prime_music_accounts = []  # List to store Prime Music access tokens


# Spotify configuration
SPOTIPY_CLIENT_ID = "baa400e3946f400d8f781f1ead7e0d6f"
SPOTIPY_CLIENT_SECRET = "62b1bbb701af4e01885e2885fa4a41a4"
SPOTIPY_REDIRECT_URI = "http://localhost:62908/callback"


# Prime Music configuration
PRIME_CLIENT_ID = "your_prime_client_id"
PRIME_CLIENT_SECRET = "your_prime_client_secret"
PRIME_REDIRECT_URI = "http://localhost:62908/prime_callback"


# Initialize the SpotifyAuthenticator and PrimeMusicAuthenticator
spotify_authenticator = SpotifyAuthenticator(
    SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
)

prime_music_authenticator = PrimeMusicAuthenticator(
    PRIME_CLIENT_ID, PRIME_CLIENT_SECRET, PRIME_REDIRECT_URI
)


# Get the authorization URLs
spotify_auth_url = spotify_authenticator.get_authorization_url()
prime_music_auth_url = prime_music_authenticator.get_authorization_url()


@flask_app.route("/callback")
def handle_callback():
    redirect_url = request.url

    # Check if it's a Spotify or Prime Music callback
    if "spotify" in redirect_url:
        handle_spotify_callback(redirect_url)
    elif "prime" in redirect_url:
        handle_prime_music_callback(redirect_url)

    return f"Callback received. Redirect URL: {redirect_url}"


def handle_spotify_callback(redirect_url):
    # Get the Spotify access token
    token_info = spotify_authenticator.get_access_token(redirect_url)

    if token_info and "access_token" in token_info:
        AppContext.spotify_accounts.append(token_info["access_token"])
    else:
        print("Error: Unable to get Spotify access token.")

    # Start the main application for Spotify in the main thread
    start_spotify_app()


def handle_prime_music_callback(redirect_url):
    # Get the Prime Music access token
    prime_token_info = prime_music_authenticator.get_access_token(redirect_url)

    if prime_token_info and "access_token" in prime_token_info:
        AppContext.prime_music_accounts.append(prime_token_info["access_token"])
    else:
        print("Error: Unable to get Prime Music access token.")

    # Start the main application for Prime Music in the main thread
    start_prime_music_app()


def start_spotify_app():
    # Start the main application for Spotify in the main thread
    app = QApplication(sys.argv)

    if len(AppContext.spotify_accounts) < 2:
        print("Error: At least two Spotify accounts are required.")
        return

    # Get the source Spotify account from the user
    source_account, ok = QInputDialog.getItem(
        None,
        "Choose Source Spotify Account",
        "Select the source Spotify account:",
        [f"Account {i+1}" for i in range(len(AppContext.spotify_accounts))],
        0,
        False,
    )

    if not ok:
        print("User canceled account selection.")
        return

    # Remove the selected source account from the available accounts
    source_index = int(source_account.split()[-1]) - 1
    source_access_token = AppContext.spotify_accounts.pop(source_index)

    # Get the destination Spotify account from the user
    destination_account, ok = QInputDialog.getItem(
        None,
        "Choose Destination Spotify Account",
        "Select the destination Spotify account:",
        [f"Account {i+1}" for i in range(len(AppContext.spotify_accounts))],
        0,
        False,
    )

    if not ok:
        # Return the source account back to the list if the user canceled destination selection
        AppContext.spotify_accounts.insert(source_index, source_access_token)
        print("User canceled destination selection.")
        return

    # Use the selected destination Spotify account
    destination_index = int(destination_account.split()[-1]) - 1
    destination_access_token = AppContext.spotify_accounts.pop(destination_index)

    try:
        # Modify the instantiation of SyncSpotify_Prime with source and destination access tokens
        window = SyncSpotify_Prime(source_access_token, destination_access_token)
        window.show()
        text = "Spotify app started."
        print(text)
        # Start the main event loop
        sys.exit(app.exec_())

    except Exception as e:
        print(f"Error starting Spotify app: {str(e)}")


def start_prime_music_app():
    # Start the main application for Prime Music in the main thread
    app = QApplication(sys.argv)
    window = SyncPrimeMusic(
        AppContext.prime_music_accounts[-1]
    )  # Use the latest Prime Music account
    window.show()

    text = "Prime Music app started."
    print(text)

    # Start the main event loop
    sys.exit(app.exec_())


@flask_app.route("/" or "/index")
def home():
    return render_template("index.html")


@flask_app.route("/loginSpotify")
def login_spotify():
    # Redirect to Spotify for authentication
    return redirect(spotify_auth_url)


@flask_app.route("/loginPrime")
def login_prime_music():
    # Redirect to Prime Music for authentication
    return redirect(prime_music_auth_url)


@flask_app.route("/profiles")
def accounts():
    try:
        return render_template("profiles.html")
    except Exception as e:
        print(f"Error rendering profiles.html: {str(e)}")
        return "An error occurred."


@flask_app.route("/process_data", methods=["POST"])
def process_data():
    try:
        payload = request.json
        # Process payload, make API calls, perform business logic

        # Prepare a response
        response_data = {"status": "success", "message": "Data processed successfully"}
        return jsonify(response_data), 200

    except Exception as e:
        print(f"Error processing data: {str(e)}")
        response_data = {"status": "error", "message": "An error occurred"}
        return jsonify(response_data), 500


if __name__ == "__main__":
    # Start the Flask app in the main thread
    flask_app.run(port=62908)
