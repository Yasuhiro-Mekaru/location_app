import logging

from dao import db_controller


class User_session(object):
	def __init__(self, session_infos, table):
		self.session_id = session_infos.get('session_id')
		self.user_master_id = session_infos.get('user_master_id')
		self.user_route_id = session_infos.get('user_route_id')
		self.user_point_id = session_infos.get('user_point_id')
		self.table = table

		self.infos = {
			'session_id': self.session_id,
			'user_master_id': self.user_master_id,
			'user_route_id': self.user_route_id,
			'user_point_id': self.user_point_id
		}


	def is_exist(self):
		datas = db_controller.get_user_session(table=self.table, kwargs=self.infos)
		return datas


	def insert_datas(self):
		db_controller.insert_user_session(table=self.table, kwargs=self.infos)


	def get_datas(self):
		datas = db_controller.get_session_datas(table=self.table, kwargs=self.infos)
		return datas