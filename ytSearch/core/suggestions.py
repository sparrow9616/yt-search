import copy
import json
import re
from typing import Union
from urllib.parse import urlencode, urlparse, parse_qs

from ytSearch.core.requests import RequestCore
from ytSearch.core.handlers import ComponentHandler
from ytSearch.core.constants import *


class SuggestionsCore(RequestCore, ComponentHandler):
    '''Backs the suggested/related videos shown beside a video on YouTube.

    Search uses `/youtubei/v1/search`; the related rail comes from
    `/youtubei/v1/next`, keyed by a video id instead of a query.
    '''

    def __init__(self, videoId: str, limit: int, language: str, region: str, timeout: int):
        super().__init__()
        self.videoId = self._extractVideoId(videoId)
        self.limit = limit
        self.language = language
        self.region = region
        self.timeout = timeout
        self.continuationKey = None
        self.autoplay = None
        self.response = None
        self.responseSource = None
        self.resultComponents = []

    def _extractVideoId(self, video: str) -> str:
        '''Accepts a bare id, a watch URL, or a youtu.be link.'''
        if not video:
            raise ValueError('ERROR: A video id or link is required.')
        if not video.startswith('http'):
            return video
        parsed = urlparse(video)
        if parsed.netloc.endswith('youtu.be'):
            return parsed.path.lstrip('/')
        videoId = parse_qs(parsed.query).get('v', [None])[0]
        if not videoId:
            match = re.search(r'/(?:shorts|embed|v)/([^/?&#]+)', parsed.path)
            videoId = match.group(1) if match else None
        if not videoId:
            raise ValueError('ERROR: Could not extract a video id from %r.' % video)
        return videoId

    def sync_create(self):
        self.continuationKey = None
        self.resultComponents = []
        self._makeRequest()
        self._parseSource()
        self._getComponents()
        while len(self.resultComponents) < self.limit and self.continuationKey:
            self._makeRequest()
            self._parseSource()
            self._getComponents()

    def _getRequestBody(self):
        requestBody = copy.deepcopy(requestPayload)
        requestBody['context']['client']['hl'] = self.language
        requestBody['context']['client']['gl'] = self.region
        if self.continuationKey:
            requestBody['continuation'] = self.continuationKey
        else:
            requestBody['videoId'] = self.videoId
        self.url = 'https://www.youtube.com/youtubei/v1/next' + '?' + urlencode({
            'key': searchKey,
        })
        self.data = requestBody

    def _makeRequest(self) -> None:
        self._getRequestBody()
        request = self.syncPostRequest()
        try:
            self.response = request.text
        except:
            raise Exception('ERROR: Could not make request.')

    async def _makeAsyncRequest(self) -> None:
        self._getRequestBody()
        request = await self.asyncPostRequest()
        try:
            self.response = request.text
        except:
            raise Exception('ERROR: Could not make request.')

    def _parseSource(self) -> None:
        try:
            response = json.loads(self.response)
            if self.continuationKey:
                self.responseSource = self._getValue(response, suggestionsContinuationPath)
            else:
                self.responseSource = self._getValue(response, suggestionsPath)
                self.autoplay = self._getValue(response, autoplayVideoIdPath)
            self.continuationKey = None
            for element in self.responseSource or []:
                if continuationItemKey in element:
                    self.continuationKey = self._getValue(element, continuationKeyPath)
        except:
            raise Exception('ERROR: Could not parse YouTube response.')

    def _getComponents(self) -> None:
        '''Appends across pages, so `resultComponents` is not reset here.'''
        for element in self.responseSource or []:
            if len(self.resultComponents) >= self.limit:
                break
            component = self._getSuggestionComponent(element)
            if component:
                self.resultComponents.append(component)

    def result(self, mode: int = ResultMode.dict) -> Union[str, dict]:
        '''Returns the suggested videos.

        Args:
            mode (int, optional): Sets the type of result. Defaults to ResultMode.dict.

        Returns:
            Union[str, dict]: Returns JSON or dictionary.
        '''
        if mode == ResultMode.json:
            return json.dumps({'result': self.resultComponents}, indent=4)
        elif mode == ResultMode.dict:
            return {'result': self.resultComponents}

    async def _nextAsync(self) -> dict:
        self.continuationKey = None
        self.resultComponents = []
        await self._makeAsyncRequest()
        self._parseSource()
        self._getComponents()
        while len(self.resultComponents) < self.limit and self.continuationKey:
            await self._makeAsyncRequest()
            self._parseSource()
            self._getComponents()
        return {
            'result': self.resultComponents,
        }
