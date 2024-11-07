import datetime

class Comment(object):
	def __init__(self, author: str, date: datetime.datetime, profile_picture: str, content_id: str) -> None:
		self.author = author
		self.date = date
		self.profile_picture = profile_picture
		self.content_id = content_id
	
	def serialize(self):
		return {
			'author': self.author, 
			'date': int(self.date * 1000),
			'profile_picture': self.profile_picture,
			'content_id': self.content_id,
		}