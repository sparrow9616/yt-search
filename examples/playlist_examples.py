
import asyncio
from ytSearch import Playlist


async def example_get_full_playlist():
    """Example: Get full playlist with info and videos"""
    print("\n" + "="*60)
    print("Example 1: Playlist.get() - Full playlist")
    print("="*60)
    
    playlist = await Playlist.get('https://www.youtube.com/playlist?list=PLRBp0Fe2Gpgn8Y9qI-p0aTxVtw8onBSFj')
    
    if playlist:
        info = playlist['info']
        videos = playlist['videos']
        
        print(f"Title: {info['title']}")
        print(f"ID: {info['id']}")
        print(f"Total Videos: {info['videoCount']}")
        print(f"Views: {info['viewCount']}")
        print(f"Channel: {info.get('channel', {}).get('name', 'N/A')}")
        print(f"\nFirst 5 videos:")
        for i, video in enumerate(videos[:5], 1):
            print(f"  {i}. {video['title']}")
            print(f"     Duration: {video['duration']}, Channel: {video['channel']['name']}")


async def example_get_info_only():
    """Example: Get only playlist information"""
    print("\n" + "="*60)
    print("Example 2: Playlist.getInfo() - Info only")
    print("="*60)
    
    info = await Playlist.getInfo('https://www.youtube.com/playlist?list=PLRBp0Fe2Gpgn8Y9qI-p0aTxVtw8onBSFj')
    
    if info:
        print(f"Playlist: {info['title']}")
        print(f"ID: {info['id']}")
        print(f"Videos: {info['videoCount']}")
        print(f"Views: {info['viewCount']}")
        if 'channel' in info:
            print(f"By: {info['channel']['name']}")
            print(f"Channel Link: {info['channel'].get('link', 'N/A')}")


async def example_get_videos_only():
    """Example: Get only playlist videos"""
    print("\n" + "="*60)
    print("Example 3: Playlist.getVideos() - Videos only")
    print("="*60)
    
    result = await Playlist.getVideos('https://www.youtube.com/playlist?list=PLRBp0Fe2Gpgn8Y9qI-p0aTxVtw8onBSFj')
    
    if result:
        videos = result['videos']
        print(f"Retrieved {len(videos)} videos\n")
        
        for i, video in enumerate(videos[:10], 1):
            print(f"{i:2}. {video['title'][:60]}")
            print(f"    🕐 {video['duration']} | 👤 {video['channel']['name']}")


async def example_pagination():
    """Example: Fetch all videos using pagination"""
    print("\n" + "="*60)
    print("Example 4: Playlist() - Fetch all with pagination")
    print("="*60)
    
    # Use a larger playlist for better pagination example
    playlist = Playlist('https://www.youtube.com/playlist?list=PLRBp0Fe2GpgnIh0AiYKh7o7HnYAej-5ph')
    
    # Initial fetch
    await playlist.getNextVideos()
    print(f"✓ Initial fetch complete")
    print(f"  Playlist: {playlist.info['title']}")
    print(f"  Videos fetched: {len(playlist.videos)}")
    print(f"  More available: {playlist.hasMoreVideos}")
    
    # Keep fetching while more videos are available
    fetch_count = 1
    while playlist.hasMoreVideos and fetch_count < 5:  # Limit to 5 fetches for demo
        print(f"\n⏳ Fetching batch {fetch_count + 1}...")
        await playlist.getNextVideos()
        print(f"  Total videos now: {len(playlist.videos)}")
        print(f"  More available: {playlist.hasMoreVideos}")
        fetch_count += 1
    
    print(f"\n📊 Final Results:")
    print(f"  Total videos fetched: {len(playlist.videos)}")
    print(f"  Has more videos: {playlist.hasMoreVideos}")
    
    print(f"\n📝 Random samples:")
    import random
    samples = random.sample(playlist.videos, min(5, len(playlist.videos)))
    for video in samples:
        print(f"  • {video['title'][:70]}")


async def example_from_video_url():
    """Example: Extract playlist from a video URL with playlist parameter"""
    print("\n" + "="*60)
    print("Example 5: Playlist from video URL")
    print("="*60)
    
    # URL with video and playlist
    url = 'https://www.youtube.com/watch?v=K4DyBUG242c&list=PLRBp0Fe2Gpgn8Y9qI-p0aTxVtw8onBSFj'
    
    playlist = await Playlist.get(url)
    
    if playlist:
        info = playlist['info']
        print(f"✓ Extracted playlist from video URL")
        print(f"  Playlist: {info['title']}")
        print(f"  Videos: {len(playlist['videos'])}")


async def example_error_handling():
    """Example: Handling invalid playlist URLs"""
    print("\n" + "="*60)
    print("Example 6: Error handling")
    print("="*60)
    
    invalid_url = 'https://www.youtube.com/playlist?list=INVALID_ID_123'
    
    result = await Playlist.get(invalid_url)
    
    if result is None:
        print("✗ Playlist not found or invalid URL")
        print("  Returns None for invalid playlists")
    else:
        print(f"✓ Playlist found: {result['info']['title']}")


async def main():
    """Run all examples"""
    print("\n" + "🎵" * 30)
    print("YouTube Playlist Examples - ytSearch Library")
    print("🎵" * 30)
    
    await example_get_full_playlist()
    await example_get_info_only()
    await example_get_videos_only()
    await example_pagination()
    await example_from_video_url()
    await example_error_handling()
    
    print("\n" + "="*60)
    print("✓ All examples completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
