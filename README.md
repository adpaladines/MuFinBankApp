# MuFinBankApp


#### SQLite installation:
1. Install SQLite (Skip if you already have it installed)
    Visit the SQLite website (https://www.sqlite.org/download.html) and download the appropriate binary for your operating system.
    Install SQLite on your machine following the installation instructions provided on their website.

2. Create a new SQLite database
    Open your terminal or command prompt.
    Run the following command to create a new SQLite database file (e.g., "banking.db"):
        
        sqlite3 banking.db

3. Create tables in the database as needed:
    With the SQLite prompt open, you can create the necessary tables for your banking database using SQL queries. For simplicity, let's create one table for planets:
        
        CREATE TABLE planets (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );

        

#### How to run server:
* Verify that every file has permissions for reading and writing.
* Open terminal 
* Go to `sqlite` directory
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
