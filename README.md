# TM Fetch Album Art

## Description

`TM Fetch Album Art` is a Python script that retrieves high-resolution album art for a given artist and album using a Apple's iTunes API.

I tend to create playlists from entire albums but Apple Music doesn't use the album artwork as the playlist artwork. I use this script to grab the image and then manually add it to my playlists.

This script can be used to enhance your music collection with high-quality album covers.

## Features

- Fetches high-resolution album art from the iTunes API
- Simple command-line interface

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/tommcfarlin/tm-fetch-album-art.git
   ```

2. **Navigate to the Project Directory**

    ```bash
    cd tm-fetch-album-art
    ```

3. **Create and Activate a Virtual Environment:**

    For macOS:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

    For Windows:

    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

4. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```


5. **Set Up Environment Variables (for Spotify)**

   If you plan to use the Spotify service, you need to create a `.env` file in the project root directory with your Spotify API credentials:

   ```
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   ```

   Replace `your_spotify_client_id` and `your_spotify_client_secret` with your actual Spotify API credentials.

## Usage

Using the script consists of adding the following in your terminal:

```bash
python fetch-album-art.py --artist="Artist Name" --album="Album Title" --service="apple"
```

Replace "Artist Name" and "Album Title" with the desired artist and album names. If you want to use Spotify, then replace "apple" with "spotify" in the `--service` parameter.

## Example

To fetch album art for "The Dark Side of the Moon" by Pink Floyd:

```bash
python fetch-album-art.py --artist="Pink Floyd" --album="The Dark Side of the Moon" --servicce="apple"
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

Thanks to the following APIs:
* [Apple](https://itunes.apple.com/search)
* [Spotify API](https://developer.spotify.com/documentation/web-api/)
