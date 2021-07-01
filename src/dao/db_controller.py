import logging

from dao import database


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_work_master():
	table = 'work_master'
	work_master = database.Work_master(table=table)
	# table名 + queryストリングスを作成し、DBクラスのインスタンスに渡してあげる
	datas = []
	query_str = 'SELECT * FROM {table}'
	kwargs = {
		'table': table,
	}
	datas = work_master.select_database(query_str=query_str, kwargs=kwargs)
	logger.info({
			'action': 'db_controller.py get_work_master',
			'datas': datas,
			'datas type': type(datas)
		})
	return datas


def insert_user_data(table, kwargs):
	# user_masterインスタンスを生成
	user_master = database.User_master(table=table)

	# table名 + queryストリングスを作成し、DBクラスのインスタンスに渡してあげる
	query_str = 'INSERT INTO {table}(name, kana_name, address, postal_number, phone_number, email_address, birth, gender, login_id, login_password, work_id)'\
				' Values("{name}","{kana_name}", "{address}", "{postal_number}", "{phone_number}", "{email_address}", "{birth}", "{gender}", "{login_id}", "{login_password}", "{work_id}")'
	kwargs['table'] = table
	user_master.exec_database(query_str=query_str, kwargs=kwargs)


def get_user_data(kwargs, is_pswd):
	# user_masterインスタンスを生成
	user_master = database.User_master(table=kwargs['table'])
	datas = []
	if is_pswd:
		query_str = 'SELECT * FROM {table} WHERE login_id="{login_id}" AND login_password="{login_password}"'
	else:
		# table名 + queryストリングスを作成し、DBクラスのインスタンスに渡してあげる
		query_str = 'SELECT * FROM {table} WHERE email_address="{email_address}"'
	datas = user_master.select_database(query_str=query_str, kwargs=kwargs)
	logger.info({
			'action': 'db_controller.py get_user_data',
			'datas': datas
		})
	return datas


def insert_user_session(table, kwargs):
	# user_sessionインスタンスを生成
	user_session = database.User_session(table=table)
	query_str = 'INSERT INTO {table}(session_id, user_master_id, user_route_id, user_point_id)'\
				' Values("{session_id}","{user_master_id}","{user_route_id}","{user_point_id}")'
	kwargs['table'] = table
	user_session.exec_database(query_str=query_str, kwargs=kwargs)


def get_user_session(table, kwargs):
	# user_sessionインスタンスを生成
	user_session = database.User_session(table=table)
	# ※session_idは一意の値になるはずなので、user_master_idの取得も含めるか 要検討！
	query_str = 'SELECT * FROM {table} WHERE session_id="{session_id}" AND user_master_id="{user_master_id}"'
	kwargs['table'] = table
	datas = user_session.select_database(query_str=query_str, kwargs=kwargs)
	logger.info({
			'action': 'db_controller.py get_user_session',
			'datas': datas
		})
	return datas


def get_session_datas(table, kwargs):
	user_session = database.User_session(table=table)
	query_str = 'SELECT * FROM {table} WHERE session_id="{session_id}"'
	kwargs['table'] = table
	datas = user_session.select_database(query_str=query_str, kwargs=kwargs)
	logger.info({
			'action': 'db_controller.py get_session_datas',
			'datas': datas
		})
	return datas


def get_current_datas(table):
	route_transaction = database.Route_transaction(table=table)
	query_str = 'SELECT * FROM {table} WHERE is_end=0'
	kwargs['table'] = table
	datas = route_transaction.select_database(query_str=query_str, kwargs=kwargs)
	return datas


def insert_user_myplace(kwargs):
	user_myplace = database.User_myplace(table=kwargs['table'])
	query_str = 'INSERT INTO {table}(name, latitude, longitude, user_master_id)'\
				' Values("{name}", "{latitude}", "{longitude}", "{user_master_id}")'
	user_myplace.exec_database(query_str=query_str, kwargs=kwargs)


def get_user_myplaces(kwargs):
	user_myplace = database.User_myplace(table=kwargs['table'])
	query_str = 'SELECT * FROM {table} WHERE user_master_id="{user_master_id}"'
	myplaces = user_myplace.select_database(query_str=query_str, kwargs=kwargs)
	logger.info({
			'action': 'db_controller.py get_user_myplaces',
			'myplaces': myplaces,
			'myplaces type': type(myplaces)
		})
	return myplaces


def get_user_myplace(kwargs):
	user_myplace = database.User_myplace(table=kwargs['table'])
	query_str = 'SELECT * FROM {table} WHERE user_myplace_id="{user_myplace_id}"'
	myplace = user_myplace.select_database(query_str=query_str, kwargs=kwargs)
	logger.info({
			'action': 'db_controller.py get_user_myplace',
			'myplaces': myplace,
			'myplaces type': type(myplace)
		})
	return myplace


def delete_user_myplace(kwargs):
	user_myplace = database.User_myplace(table=kwargs['table'])
	query_str = 'DELETE FROM {table} WHERE user_myplace_id="{user_myplace_id}"'
	user_myplace.exec_database(query_str=query_str, kwargs=kwargs)







	