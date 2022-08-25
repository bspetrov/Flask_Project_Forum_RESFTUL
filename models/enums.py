from enum import Enum


class UserRole(Enum):
    simple_user = "user"
    manager = "manager"


class ThreadState(Enum):
    open = "open"
    closed = "closed"


class ThreadCategories(Enum):
    no_category = "no category"
    gaming = "gaming"
    movies = "movies"
    books = "books"
    politics = "politics"
    social_media = "social media"
    tech_help = "technical help"
