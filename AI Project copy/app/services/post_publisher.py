from app.routes.content import publish_post_and_create_analytics

def publish_post_by_id(post_id: int):
    """
    Publish a post by its ID using the existing mock publishing function.
    This function is called by the scheduler.
    """
    return publish_post_and_create_analytics(post_id)