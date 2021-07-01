import logging

from dao import db_controller
from models import user
from models import utils
from models import sessions


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def user_sign_up(datas):
	"""ユーザーが「サインアップ」ボタンをタップした際の処理
	Args:
		datas (ImmutableMultiDict): formから送られてきたデータ
	Returns:
		message: str
		login_id: str
	"""
	name = datas.get('full_name')
	kana_name = datas.get('kana_name')
	address = datas.get('address')
	postal_number = datas.get('postal')
	phone_number = datas.get('phone_number')
	email_address = datas.get('email_address')
	birth = datas.get('birth')
	gender = datas.get('gender')
	login_id = datas.get('login_id')
	password = datas.get('password')
	work_index = datas.get('work_index')

	#passwordをハッシュ化
	hashed_pswd = utils.get_digest(user_pswd=password)
	# work_indexをintへキャスト
	work_id = int(work_index)

	user_infos = {
		'name': name,
		'kana_name': kana_name,
		'address': address,
		'postal_number': postal_number,
		'phone_number': phone_number,
		'email_address': email_address,
		'birth': birth,
		'gender': gender,
		'login_id': login_id,
		'login_password': hashed_pswd,
		'work_id': work_id
	}
	new_user = user.User(user_infos=user_infos)
	table = 'user_master'
	is_pswd = False
	# 既にユーザー登録されていないか確認
	is_user = new_user.is_exist(table=table, is_pswd=is_pswd)
	logger.info({
			'action': 'model.py user_sign_up',
			'is_user': is_user,
			'is_user type: ': type(is_user)
		})
	if not is_user:
		new_user.sign_up(table=table)
		message = 'ユーザー情報を登録しました。'
	else:
		message = 'このユーザーは登録済みです。'
	return message, new_user.login_id


def user_sign_in(datas):
	"""ユーザーが「サインイン」ボタンをタップした際の処理
	Args:
		datas (ImmutableMultiDict): formから送られてきたデータ
	Returns:
		message: str
		login_id: str
		result: str
	"""
	login_id = datas.get('login_id')
	password = datas.get('password')
	#passwordをハッシュ化
	hashed_pswd = utils.get_digest(user_pswd=password)
	user_infos = {
		'login_id': login_id,
		'login_password': hashed_pswd
	}
	new_user = user.User(user_infos=user_infos)
	table = 'user_master'
	is_pswd = True
	is_user = new_user.is_exist(table=table, is_pswd=is_pswd)
	if is_user:
		login_id = is_user[0].get('login_id')
		user_id = is_user[0].get('user_master_id')
		message = 'ようこそ'
		result = True
	else:
		login_id = ''
		user_id = ''
		message = 'ユーザーネームもしくはパスワードが違います。再度ログインしてください。'
		result = False
	logger.info({
			'action': 'model.py user_sign_in',
			'user_id': user_id,
			'user_id type': type(user_id)
		})
	return message, login_id, result, user_id


def get_work_datas():
	datas = db_controller.get_work_master()
	logger.info({
			'action': 'model.py get_work_datas',
			'datas': datas
		})
	return datas


def insert_session_id(session_id, user_id, route_id=None, point_id=None):
	session_infos = {
		'session': session_id,
		'user_master_id': user_id,
		'user_route_id': route_id,
		'user_point_id': point_id
	}
	table = 'user_session'
	db_controller.insert_user_session(table=table, kwargs=session_infos)


def start_session(session_id):
	# session_idをuser_master_idとsession_idに分割する
	session_datas = session_id.split('_')
	user_master_id = int(session_datas[1])
	session_infos = {
		'user_master_id': user_master_id,
		'session_id': session_id
	}
	table = 'user_session'
	user_session = sessions.User_session(session_infos=session_infos, table=table)
	is_session = user_session.is_exist()
	if not is_session:
		user_session.insert_datas()


def get_session_data(session_id):
	session_infos = {
		'session_id': session_id
	}
	table = 'user_session'
	user_session = sessions.User_session(session_infos=session_infos, table=table)
	session_data = user_session.get_datas()
	return session_data


def get_route_datas():
	datas = db_controller.get_current_datas()
	'''
	datasの中から
	・ from_latLngとto_latLng
	・ now_latLng
	・ is_max
	の値をdictで返す
	'''
	return datas


def regist(datas, session_id):
	session_data = get_session_data(session_id=session_id)
	datas['user_master_id'] = session_data[0]['user_master_id']
	datas['table'] = 'user_myplace'
	db_controller.insert_user_myplace(kwargs=datas)


def get_myplace_datas(session_id):
	session_data = get_session_data(session_id=session_id)
	datas = {}
	datas['user_master_id'] = session_data[0]['user_master_id']
	datas['table'] = 'user_myplace'
	myplaces = db_controller.get_user_myplaces(kwargs=datas)
	return myplaces


def get_myplace_data(user_myplace_id):
	datas = {}
	datas['user_myplace_id'] = user_myplace_id
	datas['table'] = 'user_myplace'
	try:
		myplace = db_controller.get_user_myplace(kwargs=datas)
		myplace[0]['error'] = 0
	except MYSQLdb.ERROR as e:
		logger.info({
				'action': 'app.py make_root',
				'MYSQLdb.ERROR': e
			})
		myplace = []
		data = {'error': 1}
		myplace.append(data)
	return myplace


def delete_myplace_data(datas):
	datas['table'] = 'user_myplace'
	db_controller.delete_user_myplace(kwargs=datas)


 















