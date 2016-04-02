from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
role = Table('role', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=20)),
)

roles = Table('roles', post_meta,
    Column('user_id', Integer),
    Column('role_id', Integer),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('login', String(length=40)),
    Column('email', String(length=254)),
    Column('password', String(length=160)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['role'].create()
    post_meta.tables['roles'].create()
    post_meta.tables['user'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['role'].drop()
    post_meta.tables['roles'].drop()
    post_meta.tables['user'].drop()
