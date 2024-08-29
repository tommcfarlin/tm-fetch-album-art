import requests  # type: ignore
import argparse
import os
import base64
import dotenv  # type: ignore

dotenv.load_dotenv()


def ensure_env_file_exists():
    """
    Check if the .env file exists, and create it if it doesn't.
    """
    env_file = '.env'
    if not os.path.exists(env_file):
        print(f"'{env_file}' not found. Creating it...")
        with open(env_file, 'w') as f:
            f.write("SPOTIFY_CLIENT_ID=\n")
            f.write("SPOTIFY_CLIENT_SECRET=\n")
        print(f"'{env_file}' created. Please fill in your Spotify API credentials.")
    else:
        print(f"'{env_file}' found.")


def create_images_directory():
    """
    Creates a directory named 'images' if it doesn't already exist.

    This function checks for the presence of an 'images' directory in the current
    working directory. If the directory doesn't exist, it creates one. If it
    already exists, it simply notifies the user.

    Returns:
        None
    """
    images_dir = "images"
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
        print(f"Created '{images_dir}' directory")
    else:
        print(f"'{images_dir}' directory already exists")


def create_platform_directories():
    """
    Creates 'apple' and 'spotify' subdirectories within the 'images' directory.

    This function checks for the presence of 'apple' and 'spotify' subdirectories
    in the 'images' directory. If they don't exist, it creates them. If they
    already exist, it notifies the user.

    Returns:
        None
    """
    platforms = ['apple', 'spotify']
    for platform in platforms:
        platform_dir = os.path.join('images', platform)
        if not os.path.exists(platform_dir):
            os.makedirs(platform_dir)
            print(f"Created '{platform_dir}' directory")
        else:
            print(f"'{platform_dir}' directory already exists")


def fetch_album_art_apple(artist_name, album_name):
    """
    Fetches album art from Apple Music (iTunes) for a given artist and album.

    This function uses the iTunes Search API to find the album artwork
    for the specified artist and album. It downloads the highest resolution
    image available and saves it in the 'images/apple' directory.

    Args:
        artist_name (str): The name of the artist.
        album_name (str): The name of the album.

    Returns:
        None

    Side effects:
        - Prints status messages to the console.
        - Creates a file in the 'images/apple' directory if successful.
    """
    # Base URL for iTunes Search API
    url = "https://itunes.apple.com/search"

    # Parameters for the search query
    params = {
        "term": f"{artist_name} {album_name}",
        "media": "music",
        "entity": "album",
        "limit": 1
    }

    # Make the request to the API
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Failed to retrieve data from iTunes API")
        return None

    # Parse the JSON response
    data = response.json()

    if len(data['results']) == 0:
        print("No album found for the given artist and album name")
        return None

    # Extract the artwork URL
    album_info = data['results'][0]
    artwork_url = album_info['artworkUrl100']

    # Modify the URL to get the highest resolution image available
    high_res_artwork_url = artwork_url.replace("100x100", "10000x10000")

    # Download the image
    image_response = requests.get(high_res_artwork_url)

    if image_response.status_code == 200:
        image_filename = f"{album_name} - {artist_name}.jpg"
        # Create the full path for the image file
        image_path = os.path.join("images", "apple", image_filename)

        # Ensure the apple subdirectory exists
        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        # Update the image_filename to use the new path
        image_filename = image_path
        with open(image_filename, 'wb') as image_file:
            image_file.write(image_response.content)
        print(f"Album art saved as '{image_filename}'")
    else:
        print("Failed to download the album art")


def get_spotify_access_token(client_id, client_secret):
    """
    Retrieves an access token from the Spotify API using client credentials.

    This function authenticates with the Spotify API using the provided client ID
    and client secret, and obtains an access token for making authorized requests.

    Args:
        client_id (str): The Spotify API client ID.
        client_secret (str): The Spotify API client secret.

    Returns:
        str: The access token if successful.

    Raises:
        Exception: If the request to obtain the access token fails.
    """
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_header = base64.b64encode(
        f"{client_id}:{client_secret}".encode()).decode()

    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}
    response = requests.post(auth_url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception("Failed to get access token")


def fetch_album_art_spotify(artist_name, album_name):
    """
    Fetches album art from Spotify for a given artist and album.

    This function searches the Spotify API for an album matching the provided
    artist name and album name. If found, it downloads and saves the album
    artwork.

    Args:
        artist_name (str): The name of the artist.
        album_name (str): The name of the album.

    Returns:
        None

    Side effects:
        - Prints status messages to the console.
        - Saves the album artwork as a JPG file in the 'images/spotify' directory
          if successful.
    """
    access_token = get_spotify_access_token(
        os.getenv('SPOTIFY_CLIENT_ID'), os.getenv('SPOTIFY_CLIENT_SECRET'))
    # Spotify API endpoint for search
    url = "https://api.spotify.com/v1/search"

    # Parameters for the search query
    params = {
        "q": f"artist:{artist_name} album:{album_name}",
        "type": "album",
        "limit": 1
    }

    # You need to set up Spotify API credentials and get an access token
    # This is a placeholder for the access token
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    query = f"artist:{artist_name} album:{album_name}"

    # Update the search query parameters
    params = {
        "q": query,
        "type": "album",
        "limit": 1
    }

    print(f"Searching for: {query}")

    # Make the request to the Spotify API
    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        print("Failed to retrieve data from Spotify API")
        return None

    # Parse the JSON response
    data = response.json()

    if len(data['albums']['items']) == 0:
        print("No album found for the given artist and album name")
        return None

    # Extract the artwork URL
    album_info = data['albums']['items'][0]
    artwork_url = album_info['images'][0]['url']  # Get the largest image

    # Download the image
    image_response = requests.get(artwork_url)

    if image_response.status_code == 200:
        image_filename = f"{album_name} - {artist_name}.jpg"
        # Create the full path for the image file
        image_path = os.path.join("images", "spotify", image_filename)

        # Ensure the spotify subdirectory exists
        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        # Update the image_filename to use the new path
        image_filename = image_path
        with open(image_filename, 'wb') as image_file:
            image_file.write(image_response.content)
        print(f"Album art saved as '{image_filename}'")
    else:
        print("Failed to download the album art")


def main():
    """
    Main function to handle command-line arguments and execute the album art fetching process.

    This function sets up an argument parser to accept artist name, album name, and service choice
    (Apple Music or Spotify) from the command line. It then creates necessary directories and calls
    the appropriate function to fetch album art based on the specified service.

    Command-line Arguments:
        --artist (str): Name of the artist (required)
        --album (str): Name of the album (required)
        --service (str): Service to fetch album art from (required, choices: "apple" or "spotify")

    Returns:
        None
    """

    # Setup argument parser
    parser = argparse.ArgumentParser(
        description="Fetch album art using artist and album name.")

    # Define arguments
    parser.add_argument("--artist", required=True, help="Name of the artist")
    parser.add_argument("--album", required=True, help="Name of the album")
    parser.add_argument("--service", required=True,
                        choices=["apple", "spotify"], help="Service to fetch album art from")

    # Parse arguments
    args = parser.parse_args()

    # Create necessary directories
    ensure_env_file_exists()
    create_images_directory()
    create_platform_directories()

    if args.service.lower() == "apple":
        fetch_album_art_apple(args.artist, args.album)
    elif args.service.lower() == "spotify":
        fetch_album_art_spotify(args.artist, args.album)
    else:
        print(f"Unsupported service: {args.service}")


if __name__ == "__main__":
    main()
