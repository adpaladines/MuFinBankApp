# MuFinBankApp

#### How to run server:
* Verify that every file has permissions for reading and writing.
* Open terminal 
* Go to sqlite directory
* Execute the following commands:

    - `chmod +w generate_database.py`
    - `chmod +w run_app.sh`

    - `source venv/bin/activate`
    - `python generate_database.py`
    - `python app.py`

#### Closing server:
- `CTRL+C` to extix server
- `deactivate`


#### Generating ApiDoc:
* Be sure to have npm instlled.
* Open Terminal
* Go to sqlite directory
* Execute de following command:
    - `mkdir apidoc`
    - `apidoc -i ./ -o ./apidoc`
