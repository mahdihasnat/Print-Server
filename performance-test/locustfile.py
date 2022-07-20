from this import d
from locust import HttpUser, TaskSet, task
import random

class TeamUser(HttpUser):

	def on_start(self):
		id = str(random.randint(0,119))
		self.login('lt'+id,'lt'+id)
	
	def login(self,username,password):
		response = self.client.get('/login/')
		csrftoken = response.cookies['csrftoken']
		self.client.post('/login/',
					{
						'username': username,
						'password': password,
						'csrfmiddlewaretoken': csrftoken
					},
					headers={
						'X-CSRFToken': csrftoken,
						'Referer': '/'
						})
	@task
	def submit(self):
		response = self.client.get('/submit/')
		csrftoken = response.cookies['csrftoken']
		self.client.post('/submit/',
					{
						'csrfmiddlewaretoken': csrftoken,
						'source_code': 'print("Hello World")',
					},
					headers={
						'X-CSRFToken': csrftoken,
						'Referer': '/'
						})

	@task
	def status(self):
		self.client.get("/status/")
	