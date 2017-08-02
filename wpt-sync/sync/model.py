from sqlalchemy import create_engine
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

import settings

Base = declarative_base()
Session = sessionmaker()
engine = None


class Sync(Base):
    __tablename__ = 'sync'

    id = Column(Integer, primary_key=True)
    bug = Column(Integer)
    pr = Column(Integer, unique=True)
    remote_branch = Column(String, unique=True)
    gecko_worktree = Column(String, unique=True)
    wpt_worktree = Column(String, unique=True)
    repository_id = Column(Integer, ForeignKey('repository.id'))
    source_id = Column(Integer, ForeignKey('branch.id'))

    closed = Column(Boolean, default=False)
    merged = Column(Boolean, default=False)

    repository = relationship("Repository")
    source = relationship("Branch")
    commits = relationship("Commit")


class Repository(Base):
    __tablename__ = 'repository'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    last_processed_commit_id = Column(Integer, ForeignKey('commit.id'))

    @classmethod
    def by_name(cls, session, name):
        return get(session, cls, name=name)


class Branch(Base):
    __tablename__ = 'branch'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class Commit(Base):
    """Commits to gecko repositories"""
    __tablename__ = 'commit'

    id = Column(Integer, primary_key=True)
    rev = Column(String(40), unique=True)

    sync_id = Column(Integer, ForeignKey('sync.id'))


def configure(config):
    global engine
    if engine is not None:
        return
    engine = create_engine(config["database"]["url"],
                           echo=config["database"]["echo"])
    Session.configure(bind=engine)


def create():
    assert engine is not None
    Base.metadata.create_all(engine)


def session():
    return Session()


def get(session, model, **kwargs):
    return session.query(model).filter_by(**kwargs).first()


def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()

    if instance:
        created = False
    else:
        kwargs.update(defaults or {})
        instance = model(**kwargs)
        session.add(instance)
        created = True

    return instance, created


if __name__ == "__main__":
    config = settings.load()
    configure(config)
    create()