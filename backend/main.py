#!/usr/bin/env python3

from app.models.engine.db_storage import init_db
from app.models.post import Post
from app.models.user import User
from app.models.comment import Comment
import asyncio


async def start():
    await init_db()


async def main():
    await start()

    # Create a new User
    user = await User(email="test5@example.com",
                      hashed_password="hashedpassword", username="test5").create()

    # Create a new Post
    post = await Post(user_id=user.id,
                      content="This is a test post",
                      media_type="image",
                      media_url="http://example.com/image.jpg").create()

    # Create a Comment and associate it with the Post
    comment = await Comment(post_id=post.id,
                            user_id=user.id,
                            content="First comment on the post").create()

    print(f"XXXXX: {comment.content}")
    # Delete a comment
    await Comment.find_one(Comment.content == "First comment on the post").delete()
    # Fetch the Post again to see the updated comments list

    try:
        print(f"YYYYYY: {comment.content}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

# Add the Comment to the Post's comments list and save the Post
    # post.comments.append(comment)
    # await post.save()
 # Fetch the Post and retrieve its comments
    # fetched_post = await Post.get(post.id)
    # comments_of_post = fetched_post.comments
    # print(comments_of_post)
