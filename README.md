# YT Search

A lightweight, modern YouTube search library with async/await support. Search for videos, channels, playlists, and retrieve complete playlist information with ease.

[![PyPI version](https://badge.fury.io/py/yt-search-py.svg)](https://pypi.org/project/yt-search-py/)
[![Python](https://img.shields.io/pypi/pyversions/yt-search-py.svg)](https://pypi.org/project/yt-search-py/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Features

✨ **Search Functionality**
- 🎥 Search for videos with filters
- 👤 Search for channels
- 📝 Search for playlists
- 🔍 Custom search with sorting options
- 🔄 Pagination support

✨ **Playlist Features**
- 📋 Get full playlist information with videos
- ℹ️ Get playlist metadata only
- 🎬 Get playlist videos only
- ♾️ Pagination for large playlists (100+ videos)

✨ **Modern API**
- ⚡ Async/await support
- 🎯 Type hints
- 🚀 Fast and lightweight
- 🛡️ No API key required

## Installation

```bash
pip install yt-search-py
```

## Quick Start

### Search for Videos

```python
import asyncio
from ytSearch import VideosSearch

async def main():
    search = VideosSearch('Python tutorials', limit=5)
    result = await search.next()
    
    for video in result['result']:
        print(f"{video['title']} - {video['link']}")

asyncio.run(main())
```

### Get Playlist Information

```python
import asyncio
from ytSearch import Playlist

async def main():
    # Get full playlist with videos
    playlist = await Playlist.get('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK')
    
    print(f"Playlist: {playlist['info']['title']}")
    print(f"Videos: {len(playlist['videos'])}")

asyncio.run(main())
```

## Requirements

- Python 3.7+
- httpx >= 0.28.1

## License

MIT License - see [LICENSE](LICENSE) file for details.
