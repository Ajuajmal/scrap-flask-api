### Run the application : local/dev

 - #### clone the project

      `git clone https://github.com/Ajuajmal/scrap-flask-api.git`

    - change dir `cd scrap-flask-api/local`

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
