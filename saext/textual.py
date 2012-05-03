"""

    saext.textual -- extensions to sqlalchemy.sql for dealing with raw sql
    ======================================================================

    Sometimes you need to construct query with raw sql and then integrate it
    with other sqlalchemy constructs. There's :func:`sqlalchemy.text` for that
    but you cannot use it for defining subqueries and the joining it to another
    query, for example. This module tries to provide that functionality.

"""

from sqlalchemy import Column, Text, literal_column
from sqlalchemy.sql.expression import (
    _Grouping, _TextClause, Alias as BaseAlias, ImmutableColumnCollection)

__all__ = ("raw_select",)

class GeneratedColumn(Column):

    def __init__(self, element, name):
        self.key = name
        self.name = name
        self.type = Text()
        self.table = element
        self.is_literal = False

class ColumnGenerator(object):

    def __init__(self, element):
        self.element = element

    def __getattr__(self, name):
        return GeneratedColumn(self.element, name)

    def __iter__(self):
        return iter([literal_column("*")])

class Alias(BaseAlias):

    def __init__(self, *args, **kw):
        super(Alias, self).__init__(*args, **kw)
        self.column_generator = ColumnGenerator(self)

    @property
    def columns(self):
        return self.column_generator

    def alias(self, name):
        return Alias(self.element, name)

class _RawSelectClause(_TextClause):

    columns = []

    def alias(self, name):
        return Alias(_Grouping(self), name)

def raw_select(*args, **kw):
    return _RawSelectClause(*args, **kw)

if __name__ == "__main__":
    from sqlalchemy import select
    s = raw_select("select 1 as a").alias("b")
    print select([1]).select_from(select([1]).alias("a").join(s, s.c.a == 1))
