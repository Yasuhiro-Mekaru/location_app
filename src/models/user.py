import logging

from dao import db_controller


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class User(object):
	"""docstring for User"""
	def __init__(self, user_infos):
		self.name = user_infos.get('name')
		self.kana_name = user_infos.get('kana_name')
		self.address = user_infos.get('address')
		self.postal_number = user_infos.get('postal_number')
		self.phone_number = user_infos.get('phone_number')
		self.email_address = user_infos.get('email_address')
		self.birth = user_infos.get('birth')
		self.gender = user_infos.get('gender')
		self.login_id = user_infos.get('login_id')
		self.login_password = user_infos.get('login_password')
		self.work_id = user_infos.get('work_id')

		self.infos = {
			'name': self.name,
			'kana_name': self.kana_name,
			'address': self.address,
			'postal_number': self.postal_number,
			'phone_number': self.phone_number,
			'email_address': self.email_address,
			'birth': self.birth,
			'gender': self.gender,
			'login_id': self.login_id,
			'login_password': self.login_password,
			'work_id': self.work_id
		}

	

	def sign_up(self, table):
		#db_controllerを呼び出してDBに登録する
		db_controller.insert_user_data(table=table, kwargs=self.infos)
		


	def is_exist(self, table, is_pswd):
		if is_pswd:
			kwargs = {
				'table': table,
				'login_id': self.login_id,
				'login_password': self.login_password
			}
		else:
			kwargs = {
				'table': table,
				'email_address': self.email_address
			}
			
		datas = db_controller.get_user_data(kwargs=kwargs, is_pswd=is_pswd)
		logger.info({
				'action': 'user.py is_exist',
				'datas': datas
			})
		return datas

