from this import d
from locust import HttpUser, TaskSet, task

class TeamUser(HttpUser):

	def on_start(self):
		self.login('t1','t1')
	
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
	