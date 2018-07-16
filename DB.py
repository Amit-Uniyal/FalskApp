import MySQLdb


class DB:
	def __init__(self):
		self.conn = MySQLdb.connect(
				host="localhost",
				port=3306,
				user="flaskuser",
				passwd="flaskpass",
				db="flaskapp"
		)

		self.c = self.conn.cursor()


	def get_users(self):
		self.c.execute("select * from users")

		users = self.c.fetchall()

		return_data = {}

		for user in users:
			return_data[int(user[0])] = {"username": user[1], 'firstname': user[2], 'lastname': user[3]}
		
		return return_data

	def add_user(self, data):
	
		try:

			self.c.execute('INSERT INTO users (username, firstname, lastname) VALUES(%s, %s, %s)',[data['username'], data['firstname'], data['lastname']])
			self.conn.commit()

		except Exception as e:
			return False, "Insertion Fail : "+str(e)

		return True, self.c.lastrowid

	def delete_user(self, username):
	
		msg = None		
		try:
			self.c.execute("SELECT * FROM users WHERE username=%s", [username,])
			if self.c.fetchone():
				self.c.execute("DELETE FROM users WHERE username=%s", [username])
				self.conn.commit()
			else:
				msg = False, username+" do not exist, make sure to enter correct username"

		except Exception as e:
			return False, "Delete Fail : "+  str(e)

		if msg:
			return msg

		return True, "Deleted user : "+username

	def update_user(self, username, data):

		msg = None
		try:
			self.c.execute("SELECT * FROM users WHERE username=%s", [username,])
			if self.c.fetchone():
				self.c.execute("UPDATE users SET firstname=%s, lastname=%s WHERE username=%s",[data['firstname'], data['lastname'], username])
				self.conn.commit()
			else:
				msg = False, username+" do not exists"
		
		except Exception as e:
			return False, "Update Fail : "+  str(e)

		if msg:
			return msg

		users = self.get_users()
		for k, v in users.items():
			if v['username'] == username:
				return True, v


if __name__ == '__main__':
		
		db = DB()
		'''
		data = {
		  'username': 'c',
		  'firstname': 'b',
		  'lastname': 'b'
		}

		#print(db.add_user(data))
		#print(db.get_users())
		#print(db.delete_user('b'))


		print(db.get_users())

		new_data = {
			'username': 'c',
			'firstname': '__a',
			'lastname': 'dude',
		}

		print(db.update_user('c', new_data))
		'''
		for each, v in db.get_users().items():
			print(each, v)
