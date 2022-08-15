from resources.auth import RegisterUserResource, \
    LoginUserResource
from resources.comment import MainCommentResource
from resources.thread import \
    UpdateThreadStatusResource, LikeUnlikeThreadResource, CommentThreadResource, MainThreadResource, \
    SingleThreadActionResource

routes = (
    (RegisterUserResource, "/register/"),
    (LoginUserResource, "/login/<type>/"),
    (MainThreadResource, "/thread/"),
    (SingleThreadActionResource, "/thread/<int:id>/"),
    (UpdateThreadStatusResource, "/thread/update-status/<action>/"),
    (LikeUnlikeThreadResource, "/thread/<action>/<int:id>/"),
    (CommentThreadResource, "/thread/add-comment/<int:id>/"),
    (MainCommentResource, "/comment/<int:id>/")
)
