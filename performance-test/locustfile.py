from locust import HttpUser, TaskSet, task, between
import random
import faker

class TeamUser(HttpUser):

	wait_time = between(5,20)

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
		code = faker.Faker().pystr(min_chars=50, max_chars=10000)
		response = self.client.get('/submit/')
		csrftoken = response.cookies['csrftoken']
		self.client.post('/submit/',
					{
						'csrfmiddlewaretoken': csrftoken,
						'source_code': code,
					},
					headers={
						'X-CSRFToken': csrftoken,
						'Referer': '/'
						})

	@task
	def status(self):
		self.client.get("/status/")
	