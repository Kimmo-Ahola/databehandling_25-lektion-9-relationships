from sqlalchemy import Integer, MetaData, String, Text, ForeignKey, create_engine
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column, Session, sessionmaker
from typing import List

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    
    # relationship. One user has many posts. Many = List
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="user")

    def __repr__(self) -> str:
        return f"<Id: {self.id}, Name: {self.name}>"

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)

    # FK
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # relationship
    user: Mapped["User"] = relationship("User", back_populates="posts")

    def __repr__(self) -> str:
        return f"<Id: {self.id}, Title: {self.title}, Content: {self.content}>"


def seed_users_and_posts(session: Session):
    count = session.query(User).count()

    if count == 0:
        user_1 = User(name="LarsSvensson")
        user_2 = User(name="Göran")

        user_1.posts = [Post(title="My first blog post", content="This is very exciting, my first blog post!"), 
                        Post(title="My second blog post", content="Let's talk about the weather! Is the snow coming soon?")]
        
        user_2.posts = [Post(title="Testing Testing Demo Testing", content="I am only testing")]

        # With the relationship we do not need to add session.add(posts), they are in the user object already!
        session.add(user_1)
        session.add(user_2)
        session.commit()


if __name__ == '__main__':
    engine = create_engine(url="sqlite:///demo.db")
    Base.metadata.create_all(engine)

    My_Session = sessionmaker(engine)

    with My_Session() as session:
        seed_users_and_posts(session)


    with My_Session() as session:
        number_of_stars = 50
        print(number_of_stars*'*')
        print("Printing using explicit join".center(number_of_stars))
        print(number_of_stars*'*')
        first_user = session.query(User).first()
        if first_user:
            results = session.query(User, Post)\
                .where(User.id == first_user.id)\
                .join(Post)\
                .all()

            for user, post in results:
                print(user, post)

        print("\n\n\n")
        print(number_of_stars*'*')
        print("Printing using my relationship".center(number_of_stars))
        print(number_of_stars*'*')
        first_user = session.query(User).first()
        if first_user:
            print(first_user, first_user.posts)