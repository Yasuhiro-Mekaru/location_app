import logging

import mysql.connector


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Database(object):
	"""docstring for Database"""
	def __init__(self, table=None):
		self.table = table
		self.host = 'database'
		self.port = 3306
		self.database = 'location'
		self.user = 'admin'
		self.password = 'password'
		self.infos = {
			'host': self.host,
			'port': self.port,
			'database': self.database,
			'user': self.user,
			'password': self.password
		}


	def exec_database(self, query_str, kwargs):
		try:
			conn = mysql.connector.connect(**self.infos)
			cursor = conn.cursor()
			cursor.execute(query_str.format(**kwargs))
			conn.commit()
			cursor.close()
			conn.close()
		except mysql.connector.Error as e:
			logger.info({
				'action': 'database.py exec_database',
				'error': e
			})


	def select_database(self, query_str, kwargs):
		try:
			conn = mysql.connector.connect(**self.infos)
			cursor = conn.cursor(dictionary=True)
			cursor.execute(query_str.format(**kwargs))
			rows = []
			for row in cursor.fetchall():
				rows.append(row)
			conn.commit()
			cursor.close()
			conn.close()
		except mysql.connector.Error as e:
			logger.info({
				'action': 'database.py select_database',
				'error': e
			})
			rows = []
		finally:
			return rows


		
class User_master(Database):
	def __init__(self, table):
		super().__init__(table)
		logger.info({
				'action': 'database.py User_master'
			})


class Work_master(Database):
	def __init__(self, table):
		super().__init__(table)
		logger.info({
				'action': 'database.py Work_master is called'
			})


class User_session(Database):
	"""docstring for User_session"""
	def __init__(self, table):
		super().__init__(table)
		logger.info({
				'action': 'database.py User_session is called'
			})


class Route_transaction(Database):
	"""docstring for Route_transaction"""
	def __init__(self, table):
		super().__init__(table)


class User_myplace(Database):
	"""docstring for User_myplace"""
	def __init__(self, table):
		super().__init__(table)
		logger.info({
				'action': 'database.py User_myplace is called'
		})
		
		
		








