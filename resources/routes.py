from resources.auth import RegisterForumUserResource, LoginForumUserResource, LoginForumManagerResource
from resources.thread import CreateThreadResource, SingleThreadResource, AllThreadsResource, UpdateThreadResource, \
    UpdateThreadStatusResource

routes = (
    (RegisterForumUserResource, "/register/"),
    (LoginForumUserResource, "/login/"),
    (LoginForumManagerResource, "/login/manager/"),
    (CreateThreadResource, "/thread/create/"),
    (SingleThreadResource, "/thread/get/<int:id>/"),
    (UpdateThreadResource, "/thread/update/<int:id>/"),
    (UpdateThreadStatusResource, "/thread/update-status/<int:id>/")
)