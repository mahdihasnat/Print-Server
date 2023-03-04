# Print-Server


### For complete deployment guide, please refer to [deploy-notes.md](deploy-notes.md)

### Create Virtual Environment
```bash
virtualenv venv
```

### Install Dependencies
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Install Dependencies (Manual)
```bash
pip install Django==4.0.5 fpdf==1.7.2
```

### Generate requirements.txt
```bash
pip freeze > requirements.txt
```


### Project Map

| Application | Models                             | views           |
|-------------|------------------------------------|-----------------|
| users       | MyUser, TeamUser, PrinterUser, Lab | 'home', 'status'|
| prints      | Prints, PrintConfiguration         | 'pdf', 'submit' |
| solo        | Singleton                          |                 |

## Model Description

| Model | Fields | Description |
|-------|--------|-------------|
| MyUser | is_team,is_printer, ... | This models is almost same as django.contrib.auth.models.User , This model is used for user authentication |
| TeamUser | user, lab, location | |
| PrinterUser | user, | |
| Lab | name |
| Prints | print_id, owner, source_code, submission_time, printing_time, status, total_page | Every print request from team user is modeled by this model |
| PrintConfiguration | paper_type, orientation, line_height, unit, font_size | This model is used by fpdf library while generating pdf from code |


## View Description

| View | Possible Redirection | Description |
|------|-----------------------|-------------|
| home | 'login', 'status', 'admin-panel' | !authenticated -> logout , is_team -> status , other -> admin-panel|
| status | 'submit' , 'logout' | Team can see status of their print requests
| submit | 'logout', 'home' | Team can submit code as print request
| pdf    |                  | Team_user -> null , other user -> pdf
| admin  | ...              | handled by django admin implementation
| admin-prints model | ...  | Auto refresging enabled if page is scrolled to the top. Scroll down a little bit to stop auto refresh. 
Control+Click on view pdf link to open pdf in new tab.	

## Production checklist
- Check if `DEBUG=False` in settings.py
- Run staticserver ( preferrably in another pc )
- add static url in settings.py
- makemigration and migrate
- add user info
- runserver
- check from team pc & printer pc
