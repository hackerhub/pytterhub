#!/usr/bin/env python

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, and_
import os

path = os.path.abspath(os.path.dirname(__file__)) + "/"
db = path + 'pytterhub.db'

engine = create_engine('sqlite:///' + db)
engine.echo = True

metadata = MetaData(engine)

if not os.path.exists(db):
	Alerts = Table('alerts', metadata,
		Column('id', Integer, primary_key = True),
		Column('date', String(8)),
		Column('time', String(8)),
		Column('msg', String(8)),
		)

	Alerts.create()
else:
	Alerts = Table('alerts', metadata, autoload = True)
