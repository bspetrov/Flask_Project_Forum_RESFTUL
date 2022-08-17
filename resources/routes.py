from resources.auth import RegisterUserResource, \
    LoginUserResource
from resources.comment import SingleCommentResource
from resources.thread import \
    ManagerThreadActionResource, MainThreadResource, \
    SingleThreadActionResource

routes = (
    (RegisterUserResource, "/register/"),
    (LoginUserResource, "/login/<type>/"),
    (MainThreadResource, "/thread/"),
    (SingleThreadActionResource, "/thread/<action>/<int:id>/"),
    (ManagerThreadActionResource, "/thread/manager/<action>/<int:id>/"),
    (SingleCommentResource, "/comment/<action>/<int:id>/")
)
