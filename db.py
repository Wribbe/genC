#!/usr/bin/env python3

import click
import os
import sys
import sqlite3
import types


import utils


fend_schema = ".sql"
fend_db = ".sqlite3"

DIRS = utils.resolve_dirs_from_makefile()

sql_main = """
DROP TABLE IF EXISTS db;
CREATE TABLE db (
  id INTEGER PRIMARY KEY AUTOINCREMENT
  ,name TEXT NOT NULL
  ,path TEXT NOT NULL
);
"""


class db_handler_class():
  attribs = types.SimpleNamespace()
  def __getattr__(self, name):
    attrib = getattr(self.attribs, name, None)
    if not attrib:
      if name == "main":
        attrib = self.attribs.name = init_main()
      else:
        attrib = self.attribs.name = None
    return attrib


handles = db_handler_class()
path_db_main = "main{}".format(fend_db)


def init_main():
  if not os.path.isfile(path_db_main):
    db = sqlite3.connect(path_db_main)
    db.cursor().executescript(sql_main)
    db.commit()
  else:
    db = sqlite3.connect(path_db_main)
  return db


def query(db, query, args=(), one=False):
  cursor = db.execute(query, args)
  results = cursor.fetchall()
  cursor.close()
  if one:
    return results[0] if results else None
  return results


def insert(db, query, values=(), commit=True):
  cursor = db.execute(query.format(','.join(["?"]*len(values))), values)
  if commit:
    db.commit()


def init(schema_sql, out="", db_name=""):

  if not out:
    out = os.path.join(".", schema_sql.replace(fend_schema,fend_db))
  elif len(out.split('.')) == 1 and not out.endswith(fend_db):
    out = "{}{}".format(out,fend_db)

  if not db_name:
    db_name = os.path.basename(schema_sql.replace(fend_schema,""))

  if not path_get_db(db_name):
    insert(handles.main, "INSERT INTO db (name, path) VALUES ({});", (db_name, out))

  db = get(db_name)
  with open(schema_sql, 'r') as f:
    db.cursor().executescript(f.read())
  db.commit()

  fmt_out = "Initialize the database {} with the schema {} and db_name {}."
  return fmt_out.format(out, schema_sql, db_name)


def path_get_db(db_name):
  q = query(handles.main, "SELECT path FROM db WHERE name IS (?)", (db_name,),
            one=True)
  if not q:
    return None
  return q[0]


def get(db_name):
  db = handles.db_name
  if not db:
    db = sqlite3.connect(path_get_db(db_name))
  return db


@click.group()
def cli():
  pass


@cli.command("init")
@click.argument("schema_sql")
@click.option('-out', '-o', help='Set output path of database.')
@click.option('-db_name', '-h', help='Specify db_name in handler.')
def cli_init(schema_sql, out, db_name):
  click.echo(init(schema_sql, out, db_name))


@cli.command()
def drop():
  click.echo("Dropped the database")


if __name__ == "__main__":
  cli()
