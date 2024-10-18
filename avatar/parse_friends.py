from PIL import Image, ImageOps, ImageDraw
import math
import requests
from io import BytesIO
from atproto import Client

def parse_friends(client: Client, handle: str) -> dict:
    friends = dict()
    def update_data(friendData):
        did = friendData.pop('did')
        if did in friends:
            friends[did]['reply_score'] += friendData['reply_score']
        else:
            friends[did] = friendData
    # Get profile's posts. Use pagination (cursor + limit) to fetch all
    profile_feed = client.get_author_feed(actor=handle)
    for feed_view in profile_feed.feed:
        if feed_view.post.record.reply != None:
            reply_parent = feed_view.post.record.reply.parent
            try:
                reply_parent_author = client.get_post_thread(reply_parent.uri).thread.post.author
            except:
                continue # Skip if the author of the parent post is not found
                
            if reply_parent_author.handle == handle:
                continue
            friendData = {
                'did': reply_parent_author.did,
                'avatar': reply_parent_author.avatar,
                'display_name': reply_parent_author.display_name,
                'reply_score': 1,
            }
            update_data(friendData)
        elif feed_view.post.author.handle == handle:
            replies = client.get_post_thread(feed_view.post.uri).thread.replies
            for reply in replies:
                if reply.post.author.handle == handle:
                    continue
                friendData = {
                    'did': reply.post.author.did,
                    'avatar': reply.post.author.avatar,
                    'display_name': reply.post.author.display_name,
                    'reply_score': 1.5,
                }
                update_data(friendData)
    
    return friends