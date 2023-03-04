Required Applications: python3,nginx,sqlite3

Steps:
1. Install dependencies: `pip3 install -r requirements.txt`	
2. * Make migrations: `python3 ./printserver/manage.py makemigrations`
	*  Migrate: `python3 ./printserver/manage.py migrate`
3. Collect static files: `python3 ./printserver/manage.py collectstatic`
4. Add user to database: `python3 printserver/manage.py shell < printserver/add_user_script.py`
5. Follow instructions in [staticserver/Readme.md](staticserver/Readme.md) to setup static server.
6. Run server: `python3 ./printserver/manage.py runserver`


All steps are combined in deploy.sh: `sudo ./deploy.sh`
