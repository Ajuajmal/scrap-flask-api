## Docs

### Tools we are using
  
  - flask :- for our api application
  - bs4 :- for scrapping
  - requests: for authenticating with linkedin
  
### Fire the api calls :
  
  - #### By using hosted application's form @ heroku 
     
     > http://scrap.code.ajmalaju.com/
      
  


### Run the application

 - #### clone the project

      `git clone https://github.com/Ajuajmal/scrap-flask-api.git`
  
    - change dir `cd scrap-flask-api`
  
 - #### create virtual env
    
      `virtualenv -p python3 env`
    
    - activate virtualenv `source env/bin/activate`
  
 - #### Install requirements
    
      `pip3 install -r requirements.txt`
      
  - #### Set Env Variables
    
      `cp .env.local .env`
      
      - edit and add the following in .env file `nano .env`
       
      - eg : -  
              
              ````
                LINKEDIN_MAIL = 'test@mail.com'
               
                LINKEDIN_PASSWORD = 'password12345'
              ````
      
      - save `.env` file by `CTRL+O` and exit the editor `CTRL+X`
    
   - # Fire the app 
       
       `flask run` 
