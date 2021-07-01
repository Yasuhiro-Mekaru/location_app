import base64
import hashlib
import os


def get_digest(user_pswd):
	"""パスワードのハッシュ値を生成する処理
	Args:
		user_pswd (str): パスワード
	Returns:
		bytes: パスワードから生成されたハッシュ値
	"""
	# ランダムな値を生成
	# salt = base64.b64encode(os.urandom(32))
	# パスワードの値をハッシュ化
	password = bytes(user_pswd, 'utf-8')
	# digest = hashlib.pbkdf2_hmac('sha256', password, salt, 10000)
	digest = hashlib.sha256(password).hexdigest()
	print('utils.py get_digest digest: ', digest)
	print('utils.py get_digest digest type: ', type(digest))

	return digest