from pythonlemmy import LemmyHttp
from pythonlemmy.responses import GetCommunityResponse, PostResponse

from .. import PostContext, PostTemplate


class PostHelper:

    @staticmethod
    def create_post(
            request: LemmyHttp,
            post_context: PostContext,
            post_template: PostTemplate
    ) -> int:
        community = PostHelper.get_community_by_name(request, post_context.community_name)
        response = PostResponse(request.create_post(
            community_id=community.community_view.community.id,
            name=post_template.title,
            body=post_template.content,
            url=post_template.link
        ))
        return response.post_view.post.id

    @staticmethod
    def get_community_by_name(
            request: LemmyHttp,
            community_name: str
    ) -> GetCommunityResponse:
        return GetCommunityResponse(request.get_community(name=community_name))

    @staticmethod
    def pin_post(
            request: LemmyHttp,
            post_id: int,
            pinned: bool
    ):
        request.feature_post(
            feature_type="Community",
            featured=pinned,
            post_id=post_id
        )
