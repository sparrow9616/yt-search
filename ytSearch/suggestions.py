from typing import Any, Dict

from ytSearch.core.constants import *
from ytSearch.core.suggestions import SuggestionsCore


class VideoSuggestions(SuggestionsCore):
    '''Fetches the videos YouTube suggests alongside a given video.

    Args:
        videoId (str): A video id, watch link or youtu.be link.
        limit (int, optional): Sets limit to the number of results. Defaults to 20.
        language (str, optional): Sets the result language. Defaults to 'en'.
        region (str, optional): Sets the result region. Defaults to 'US'.

    Examples:
        Calling `next` gives the suggested videos.

        >>> suggestions = VideoSuggestions('jADTdg-o8i0', limit = 1)
        >>> print(await suggestions.next())
        {
            "result": [
                {
                    "type": "video",
                    "id": "iJVtxex6HIk",
                    "title": "Water I Diljit Dosanjh I Happy Valentine Day",
                    "duration": "3:15",
                    "thumbnails": [
                        {
                            "url": "https://i.ytimg.com/vi/iJVtxex6HIk/hqdefault.jpg",
                            "width": 168,
                            "height": 94
                        }
                    ],
                    "channel": {
                        "name": "Diljit Dosanjh",
                        "id": "UCZRdNleCgW-BGUJf-bbjzQg",
                        "thumbnails": [
                            {
                                "url": "https://yt3.ggpht.com/7EYXXMXY594V8y4sZT2aawmdKgDAGTu5jNm9C-HpR3jY9cZJ0NMxS__nZKBdWZ1PUpJPjc2BAA=s88-c-k-c0x00ffffff-no-rj",
                                "width": 68,
                                "height": 68
                            }
                        ],
                        "link": "https://www.youtube.com/channel/UCZRdNleCgW-BGUJf-bbjzQg"
                    },
                    "viewCount": {
                        "short": "97M views",
                        "text": "97M views"
                    },
                    "publishedTime": "1 year ago",
                    "link": "https://www.youtube.com/watch?v=iJVtxex6HIk"
                }
            ]
        }

        The video YouTube would autoplay next is available after the request.

        >>> print(suggestions.autoplay)
        'iJVtxex6HIk'
    '''

    def __init__(self, videoId: str, limit: int = 20, language: str = 'en', region: str = 'US', timeout: int = None):
        super().__init__(videoId, limit, language, region, timeout)

    async def next(self) -> Dict[str, Any]:
        return await self._nextAsync()
