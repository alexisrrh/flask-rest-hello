from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column
from typing import List

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="user_enlace")
    following: Mapped[List["Follower"]] = relationship("Follower", foreign_keys="Follower.user_from_id",back_populates="user_from")

    followers: Mapped[List["Follower"]] = relationship( "Follower",foreign_keys="Follower.user_to_id",back_populates="user_to")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email
        }


class Follower(db.Model):
    __tablename__ = "follower"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    user_from: Mapped["User"] = relationship("User",foreign_keys=[user_from_id],back_populates="following")

    user_to: Mapped["User"] = relationship("User",foreign_keys=[user_to_id], back_populates="followers")
 
    def serialize(self):
        return {
            "id": self.id,
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id
        }


class Comment(db.Model):

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(300), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] =  mapped_column(ForeignKey("post.id"))
    post_enlace: Mapped["Post"] = relationship("Post", back_populates="comments_enlace")
    user_enlace: Mapped[List["User"]] = relationship(secondary="User", back_populates="comments_enlace")
    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id
        }

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    comments_enlace: Mapped[List["Comment"]] = relationship("Comment", back_populates="post_enlace")
    media_enlace: Mapped[List["Media"]] = relationship("Media", back_populates="post_enlace")
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id
        }

class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    url: Mapped[str] = mapped_column(String(200), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post_enlace: Mapped["Post"] = relationship("Post", back_populates="media_enlace")
    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "post_id": self.post_id
        }