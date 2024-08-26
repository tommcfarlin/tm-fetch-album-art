import requests
import argparse


def fetch_album_art(artist_name, album_name):
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
        with open(image_filename, 'wb') as image_file:
            image_file.write(image_response.content)
        print(f"Album art saved as '{image_filename}'")
    else:
        print("Failed to download the album art")


def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(
        description="Fetch album art using artist and album name.")

    # Define arguments
    parser.add_argument("--artist", required=True, help="Name of the artist")
    parser.add_argument("--album", required=True, help="Name of the album")

    # Parse arguments
    args = parser.parse_args()

    # Call the function with the provided arguments
    fetch_album_art(args.artist, args.album)


if __name__ == "__main__":
    main()
