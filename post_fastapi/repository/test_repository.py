from typing import List
from domain.comment import Comment
from domain.post import Post
from domain.user import User
from sqlmodel import Session, select


class TestRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_post(self, post: Post) -> Post:
        item = Post(**post)
        self.session.add(item)
        self.session.commit()

        return self.session.get(Post, item.id)

    def create_user(self, user: User) -> None:
        self.session.add(user)
        self.session.commit()

    def create_comment(self, comment: Comment) -> List[Comment]:
        self.session.add(Post(id=comment["post_id"], user_id=comment["user_id"]))

        self.session.add(Comment(**comment))
        self.session.commit()

        return self.session.exec(select(Comment)).all()

    def count_posts(self) -> int:
        return len(self.session.exec(select(Post)).all())

    def count_users(self) -> int:
        return len(self.session.exec(select(User)).all())

    def count_comments(self) -> int:
        return len(self.session.exec(select(Comment)).all())
