# cse4471-keylogger

## Adding SSL to Server
1. Navigate into the `server` folder.
2. Create a new directory using `mkdir ssl`.
3. Run `cd ssl` and then run the following command, inputting whatever you want at the prompts:

    ```
    openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
    ```

4. This will create and save your self-signed certificate to the `ssl` folder. This folder will automatically be ignored when pushing to Github.

## Setting up the Server
1. Navigate into the `server` folder.
2. Create a new python virtual environment by running `python3 -m venv venv`. This will store all your packages in the `venv` folder (which is also ignored when pushing to Github).
3. Activate your virtual environment by running `source venv/bin/activate`.
4. Run `pip install -U pip` to upgrade pip and then run `pip install -r requirements.txt` to download all the required python packages for the server.
5. After running the above commands, you will need to setup your terminal environment so that Flask can be run. Do this by running the following two commands:

    ```
    export FLASK_ENV=production
    export FLASK_APP=commandr
    ```

5. Setup the database by running `flask init-db`
6. Then, to initialize the database with fake data, run `python admin.py admin admin`. This will create the user 'admin' with the password 'admin'.
7. Finally, run Flask by running `python run.py`.

## Flask API

**Create Trojan**
----
  Creates a trojan.

* **URL**

  /api/v1/trojans/create

* **Method:**

  `POST`

*  **URL Params**

   **Required:**

   `ip=[text]`

   `port=[integer]`

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"id":1,"ip":"127.0.0.1","last_updated":"Mon, 01 Apr 2019 18:33:34 GMT","logged_text":"No logged text.","port":5000,"status":0}`

* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ error : "Resource not found" }`

* **Sample Call:**

  ```
  curl --cacert cert.pem -X POST -u admin:admin -i https://localhost:5000/api/v1/trojans/create\?ip\=127.0.0.1\&port\=5000
  ```

**Update Trojan**
----
  Updates a trojan.

* **URL**

  /api/v1/trojans

* **Method:**

  `PUT`

*  **URL Params**

   **Required:**

   `id=[integer]`
   
   **Optional:**

   `logged_text=<path to file name>`

   `status=[1|0]`

* **Data Params**

  Text File (optional)

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"id":1,"ip":"127.0.0.1","last_updated":"Mon, 01 Apr 2019 18:44:46 GMT","logged_text":"No logged text.","port":5000,"status":1}`

* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ error : "Resource not found" }`

* **Sample Call:**

  ```
  Updating Status:
  curl --cacert cert.pem -H "Content-Type: application/json" -X PUT -u admin:admin -i https://localhost:5000/api/v1/trojans\?id\=1\&status\=1

  Logging Text:
  curl --cacert cert.pem -F 'logged_text=@/Users/alec/test.txt' -X PUT -u admin:admin -i https://localhost:5000/api/v1/trojans\?id\=1
  ```
