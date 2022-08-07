from resources.auth import RegisterForumUserResource, LoginForumUserResource, LoginForumManagerResource

routes = (
    (RegisterForumUserResource, "/register/"),
    (LoginForumUserResource, "/login/"),
    (LoginForumManagerResource, "/login/manager/")
)