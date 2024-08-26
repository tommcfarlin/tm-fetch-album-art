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

## Usage

Using the script consists of adding the following in your terminal:

```bash
python fetch-album-art.py --artist="Artist Name" --album="Album Title"
```

Replace "Artist Name" and "Album Title" with the desired artist and album names.

## Example

To fetch album art for "The Dark Side of the Moon" by Pink Floyd:

```bash
python fetch-album-art.py --artist="Pink Floyd" --album="The Dark Side of the Moon"
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

Thanks to the [Apple](https://itunes.apple.com/search) for providing the album art API.
