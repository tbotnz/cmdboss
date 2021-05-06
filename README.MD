![cmdboss](cmdboss.PNG)

a **hooky** rest based nosql database that makes configuration management better

### core features
- Model driven ReST API backed by a noSQLDB (Mongo) with a Pydantic Validation
- Self generating swagger documenting Endpoints for CRUD operations for all user defined models
- Custom Middleware Layer providing async hook capability on DB CRUD operations
- BYO Python Hooks
- BYO Pydantic Models

### getting started
- git clone the project ``` https://github.com/tbotnz/cmdboss.git ```
- cd into the cmdboss dir ```cd cmdboss ```
  -  Optional (Configure config.json) with your settings
- docker comppose up ```docker-compose up --build```
- access swagger via ```http://127.0.0.1:9000/docs```
- download the online [postman collection](https://documenter.getpostman.com/view/2391814/TzRPjV5h)

