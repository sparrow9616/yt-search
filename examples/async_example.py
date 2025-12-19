from ytSearch import *
import asyncio

async def main():
    '''
    Searches for all types of results like videos, channels & playlists in YouTube.
    'type' key in the JSON/Dictionary may be used to differentiate between the types of result.
    '''
    search = Search('NoCopyrightSounds', limit = 1, language = 'en', region = 'US')
    result = await search.next()
    print(result)




    '''
    Searches only for videos in YouTube.
    '''
    videosSearch = VideosSearch('NoCopyrightSounds', limit = 10, language = 'en', region = 'US')
    videosResult = await videosSearch.next()
    print(videosResult)




    '''
    Searches only for channels in YouTube.
    '''
    channelsSearch = ChannelsSearch('NoCopyrightSounds', limit = 1, language = 'en', region = 'US')
    channelsResult = await channelsSearch.next()
    print(channelsResult)




    '''
    Searches only for playlists in YouTube.
    '''
    playlistsSearch = PlaylistsSearch('NoCopyrightSounds', limit = 1, language = 'en', region = 'US')
    playlistsResult = await playlistsSearch.next()
    print(playlistsResult)


    playlist = Playlist('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK')
    while playlist.hasMoreVideos:
        print('Getting more videos...')
        await playlist.getNextVideos()
        print(f'Videos Retrieved: {len(playlist.videos)}')

    print('Found all the videos.')




    '''
    Can be used to get search results with custom defined filters.

    Setting second parameter as VideoSortOrder.uploadDate, to get video results sorted according to upload date.

    Few of the predefined filters for you to use are:
    SearchMode.videos
    VideoUploadDateFilter.lastHour
    VideoDurationFilter.long
    VideoSortOrder.viewCount
    There are many other for you to check out.

    If this much control isn't enough then, you may pass custom string yourself by seeing the YouTube query in any web browser e.g. 
    "EgQIBRAB" from "https://www.youtube.com/results?search_query=NoCopyrightSounds&sp=EgQIBRAB" may be passed as second parameter to get only videos, which are uploaded this year.
    '''
    customSearch = CustomSearch('NoCopyrightSounds', VideoSortOrder.uploadDate, language = 'en', region = 'US')
    customResult = await customSearch.next()
    print(customResult)


    '''
    Getting search results from the next pages on YouTube.
    Generally you'll get maximum of 20 videos in one search, for getting subsequent results, you may call `next` method.
    '''
    search = VideosSearch('NoCopyrightSounds')
    index = 0
    ''' Getting result on 1st page '''
    result = await search.next()
    ''' Displaying the result '''
    for video in result['result']:
        index += 1
        print(f'{index} - {video["title"]}')
    ''' Getting result on 2nd page '''
    result = await search.next()
    ''' Displaying the result '''
    for video in result['result']:
        index += 1
        print(f'{index} - {video["title"]}')
    ''' Getting result on 3rd page '''
    result = await search.next()
    ''' Displaying the result '''
    for video in result['result']:
        index += 1
        print(f'{index} - {video["title"]}')


    '''
    Getting information about playlist or videos in it using link.

    `Playlist.get` method will give both information & videos in the playlist
    `Playlist.getInfo` method will give only information about the playlist.
    `Playlist.getFormats` method will give only formats of the playlist.

    '''
    playlist = await Playlist.get('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK')
    print(playlist)
    playlistInfo = await Playlist.getInfo('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK')
    print(playlistInfo)
    playlistVideos = await Playlist.getVideos('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK')
    print(playlistVideos)

    '''
    More tests to buggy Playlist class
    '''
    playlist = await Playlist.get('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgmsW46rJyudVFlY6IYjFBIK')
    print(playlist)
    playlist = await Playlist.get('https://www.youtube.com/watch?v=bplUXwTTgbI&list=PL6edxAMqu2xfxgbf7Q09hSg1qCMfDI7IZ')
    print(playlist)

if __name__ == '__main__':
    asyncio.run(main())