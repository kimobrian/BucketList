# BucketList API
A bucket list API designed in python Flask framework.

**Note:** `Python Version 2.7`
## Installation.
Clone from the repo [Code Modularization](https://github.com/kimobrian/BucketList)

For SSH:

`git clone -b code-modularization git@github.com:kimobrian/BucketList.git`

For https:

`git clone -b code-modularization https://github.com/kimobrian/BucketList.git`


Follow the instructions [here](http://docs.python-guide.org/en/latest/dev/virtualenvs/) to create and activate a virtual environment.

Navigate into the project directory with `cd BucketList` and install dependencies with `pip install -r requirements.txt`

## Database Configurations
Use the file `config.py` to control your database configurations and preferences:
### Postgresql
Follow the instructions [here](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0ahUKEwi1icuBqIzQAhWFIcAKHQBpAE4QFggaMAA&url=https%3A%2F%2Fwww.postgresql.org%2Fdocs%2F9.1%2Fstatic%2Ftutorial-install.html&usg=AFQjCNHokIop8EMX5GCE9tlhOYgMr1Yfpg&bvm=bv.137132246,d.d2s) to install and setup postgresql. 
Create a test database and an application database to be used for testing and running the application.
Edit the configurations in `config.py` to match you database names. Under class DevelopmentConfig, alter the following to match your application DB created:

`SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost:5432/application_database_name'`

Under TestingConfig class, make the changes as follows:

`SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost:5432/test_database_name'`

### SQLite
Uncomment the following lines to switch to SQLite and remove postgresql settings in both DevelopmentConfig and TestinngConfig classes:

```
db_path = os.path.join(os.path.dirname(__file__), 'application_db_name.sqlite')

db_uri = 'sqlite:///{}'.format(db_path)`

SQLALCHEMY_DATABASE_URI = db_uri
```
In TestingConfig class, set `TESTING = True`


Setup the database with the following commands:

```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

Run the Application with: 

`python manage.py runserver` and access the server at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

Run tests with `tox` command

## Application Endpoints/ Routes


| Resource URL | Methods | Description | Requires Token |
| -------- | ------------- | --------- |--------------- |
| `/auth/register/` | POST  | User registration | FALSE |
| `auth/register/`  | GET | View all registered users | TRUE |
|  `/auth/login/` | POST | User login | FALSE |
| `/bucketlists/` | GET, POST | A user's bucket lists | TRUE |
| `/bucketlists/<bucketlist_id>` | GET, PUT, DELETE | A single bucket list | TRUE |
| `/bucketlists/<bucketlist_id>/items/` | GET, POST | Items in a bucket list | TRUE |
| `/bucketlists/<bucketlist_id>/items/<item_id>` | GET, PUT, DELETE | A single bucket list item | TRUE |

*Pending Issues*
- `tox` command not running tests on postgresql

