from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox
import spotipy
import requests


class SyncSpotify_Prime(QWidget):
    def __init__(self, source_access_token, destination_access_token):
        super().__init__()

        # Attributes to store the access tokens
        self.source_access_token = source_access_token
        self.destination_access_token = destination_access_token

        # Fetch the user's playlists from Spotify during initialization
        self.source_playlists = self.get_user_playlists(self.source_access_token)
        self.destination_playlists = self.get_user_playlists(
            self.destination_access_token
        )

        self.init_ui()

    def init_ui(self):
        # Create layout
        layout = QVBoxLayout()

        # Create combo box for source playlist selection
        self.source_playlist_combo = QComboBox()
        self.source_playlist_combo.addItems(self.source_playlists)
        layout.addWidget(self.source_playlist_combo)

        # Create combo box for destination playlist selection
        self.destination_playlist_combo = QComboBox()
        self.destination_playlist_combo.addItems(self.destination_playlists)
        layout.addWidget(self.destination_playlist_combo)

        # Create a button for playlist synchronization
        sync_button = QPushButton("Sync Playlists")
        sync_button.clicked.connect(self.sync_playlists)
        layout.addWidget(sync_button)

        # Create a label for status display
        self.status_label = QLabel("Status: Ready")
        layout.addWidget(self.status_label)

        # Set the layout
        self.setLayout(layout)

        # Set window properties
        self.setWindowTitle("SyncSpotify Prime")
        self.setGeometry(300, 300, 300, 200)

    def sync_playlists(self):
        # Get the selected playlists from the combo boxes
        selected_source_playlist = self.source_playlist_combo.currentText()
        selected_destination_playlist = self.destination_playlist_combo.currentText()

        # Add your playlist synchronization logic here
        # For now, we'll just update the status label with the selected playlists
        self.status_label.setText(
            f"Status: Syncing {selected_source_playlist} to {selected_destination_playlist}"
        )

        # Call the method to handle playlists
        self.get_user_playlists(self.source_access_token)
        self.get_user_playlists(self.destination_access_token)

    def get_user_playlists(self, access_token):
        # Use spotipy package / module to make Spotify API requests
        sp = spotipy.Spotify(auth=access_token)

        # Example: Get the current user's playlists
        playlists = sp.current_user_playlists()

        # Check if playlists are not None and contain "items" key
        if playlists is not None and "items" in playlists:
            # Extract playlist names and return them
            return [playlist["name"] for playlist in playlists["items"]]
        else:
            print("No playlists found.")
            return []
