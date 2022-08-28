import sqlite3

cnx = sqlite3.connect('base.db')
cur = cnx.cursor()


def commit():
    cnx.commit()


def close():
	cnx.close()


def field(command, *values):
	cur.execute(command, tuple(values))

	if (fetch := cur.fetchone()) is not None:
		return fetch[0]


def record(command, *values):
	cur.execute(command, tuple(values))
	return cur.fetchone()


def records(command, *values):
	cur.execute(command, tuple(values))
	return cur.fetchall()


def column(command, *values):
	cur.execute(command, tuple(values))
	return [item[0] for item in cur.fetchall()]


def execute(command, *values):
	cur.execute(command, tuple(values))


def multiexec(command, valueset):
	cur.executemany(command, valueset)