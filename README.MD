

<p align="center">
   <br/>
   <img src="/cmdboss.PNG" />
   <br/>
   <p align="center">
      API driven, <b>integrated</b> configuration management
   </p> 
   <br/>
</p>

<hr/>

<p align="center">
   
   <br/>
   <img src="/marketecture-2.png" />
   <br/>
</p>


## Features

- Model driven REST API leveraging **FastAPI** underpinned by **Python** hooks and **Mongo** DB
- Upload your own **Pydantic** models for data validation + **Python** hooks @ Runtime over the REST interface
- Self generating **swagger** & dynamic CRUD REST endpoints for db operations of all user defined models
- Custom **hook** layer providing **async** hook capability on DB CRUD operations via a threaded queue

## Demo

![cmdboss](cboss-1.gif)

## Getting Started

- git clone the project ``` https://github.com/tbotnz/cmdboss.git ```
- cd into the cmdboss dir ```cd cmdboss ```
  -  Optional (Configure ```config.json```) with your settings
- docker comppose up ```docker-compose up --build```
- access swagger via ```http://127.0.0.1:9000/docs```
- download the online [postman collection](https://documenter.getpostman.com/view/2391814/TzRPjV5h)

![pman](cboss-pman.PNG)

## Roadmap

- GUI for real time model editing
- Add Endpoint Authorisation
- Automate reloading of models
- GraphQL support

## Community

You can also find us in the channel #cmdboss on the networktocode Slack.
