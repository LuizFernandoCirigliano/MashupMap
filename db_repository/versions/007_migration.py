from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
mashup = Table('mashup', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=300)),
    Column('author', String(length=64)),
    Column('permalink', String(length=1000)),
    Column('date', DateTime),
    Column('content', String(length=1000)),
    Column('isBroken', Boolean, default=ColumnDefault(False)),
    Column('url', String(length=1000)),
    Column('score', Integer, default=ColumnDefault(0)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['mashup'].columns['score'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['mashup'].columns['score'].drop()
