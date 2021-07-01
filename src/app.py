import json
import logging

from flask import Flask, jsonify
from flask import redirect, render_template, request, session, url_for

from models import model

app = Flask(__name__)
app.secret_key = 'test_secret_key'
app.config['JSON_AS_ASCII'] = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/', methods=['GET'])
def index():
	# Cookieチェック
	if session:
		# Cookieがある場合
		return redirect(url_for('main_menu', message='', login_id=session['session_id']))
	else:
		return render_template('index.html')


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
	if request.method == 'GET':
		message = '必要事項を入力し、ユーザー登録をしてください。'
		work_master_datas = model.get_work_datas()
		return render_template('sign_up.html', message=message, datas=work_master_datas)
	else:
		form_datas = request.form
		message, login_id = model.user_sign_up(datas=form_datas)
		return redirect(url_for('sign_in', message=message, login_id=login_id))


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
	if request.method == 'GET':
		if request.args:
			message = request.args.get('message', '')
			login_id = request.args.get('login_id', '')
		else:
			message = 'ユーザーIDとパスワードを入力してサインインしてください。'
			login_id = ''
		return render_template('sign_in.html', message=message, login_id=login_id)
	else:
		form_datas = request.form
		message, login_id, result, user_id = model.user_sign_in(datas=form_datas)

		if result:
			session_id = f'{login_id}_{user_id}'
			session['session_id'] = session_id
			# session情報をDBに格納
			# model.insert_session_id(session_id=session_id, user_id=user_id)
			model.start_session(session_id=session_id)
			return redirect(url_for('main_menu', message=message, login_id=login_id))
		else:
			return render_template('sign_in.html', message=message,
							login_id=login_id)


@app.route('/main_menu', methods=['GET'])
def main_menu():
	if session:
		if request.args:
			message = request.args.get('message', '')
			login_id = request.args.get('login_id', '')
		else:
			message = ''
			login_id = ''

		# route_transactionテーブルから現在動いているルート情報を取得し、render_templateに渡す
		# DBに値を格納するまではコメントアウト
		# current_route_datas = model.get_route_datas()
		return render_template('main_menu.html', message=message, login_id=login_id)
	else:
		# sessionが無い場合はindex.htmlにリダイレクトさせる
		return redirect(url_for('index'))


@app.route('/regist_place', methods=['GET', 'POST'])
def regist_place():
	if session:
		if request.method == 'GET':
			return render_template('regist_place.html', message='', login_id=session['session_id'])
		else:
			datas = request.get_json()
			model.regist(datas=datas, session_id=session['session_id'])
			# return json.dumps('success')
			return jsonify('success')
	else:
		return(url_for('index'))


@app.route('/get_myplace', methods=['GET'])
def get_myplace():
	if session:
		datas = model.get_myplace_datas(session_id=session['session_id'])
		return jsonify(datas)
	return jsonify('No session')


@app.route('/delete_myplace', methods=['POST'])
def delete_myplace():
	datas = request.get_json()
	model.delete_myplace_data(datas=datas)
	return jsonify('success')


@app.route('/make_root', methods=['GET', 'POST'])
def make_root():
	if request.method == 'GET':
		pass
	else:
		user_myplace_id = ''
		state = ''
		if request.form.get('arrive') is not None:
			user_myplace_id = int(request.form.get('arrive'))
			state = 'arrive'
		else:
			user_myplace_id = int(request.form.get('departure'))
			state = 'departure'	
		datas = model.get_myplace_data(user_myplace_id=user_myplace_id)
		datas[0]['state'] = state
		logger.info({
				'action': 'app.py make_root',
				'datas': datas,
				'datas type': type(datas)
			})
		return render_template('make_root.html', datas=datas)


@app.route('/firebase-messaging-sw.js')
def sw():
	logger.info({
			'action': 'firebase_messaging_sw is called'
		})
	return app.send_static_file('firebase-messaging-sw.js')



def main():
	print('Flask run!!')
	# app.run(host='0.0.0.0', port=5000, ssl_context=('../web/openssl/server.crt', '../web/openssl/server.key'), debug=True)
	app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
	main()
