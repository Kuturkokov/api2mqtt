# API 2 MQTT Server
API server to send and receive data from an MQTT server.
This was built in an attempt to have siri shortcuts integrate with my mqtt server

This will work with or without Docker.

Create a .env with the following:\
<sub> Set REG_OPEN to True if this is the first run </sub>

```
SECRET_KEY=GENERATE_A_SECURE_KEY
MQTT_SERVER=IP_OF_SERVER
REG_OPEN=False
TZ=Europe/London
```
Other optional parameters are:\
MQTT_USER=\
MQTT_PASS=\
MQTT_PORT=

### Getting started with docker
<sub> This assumes you have Docker and Docker Compose installed</sub>

1. Clone the repo

2. Navigate to the folder using your terminal
3. Run ```docker build -t api2mqtt .```
4. Once the build is complete you can run ```docker-compose up -d```

### Without Docker

1. Clone the repo
2. Create "data" and "logs" folders in the "app" folder
3. Move the .env file you created to the "config" folder in the "app" folder
4. Navigate to the project root folder using your terminal
5. Run the following commands

For Windows
```
python - m venv .
.\Scripts\activate
pip install -r requirements.txt
```
For Linux
```
python3 -m venv .
source bin/activate
python3 -m pip install -r requirements.txt
```
Navigate into "app" folder
Run ```python main.py``` for Windows or ```python3 main.py``` for Linux

## Registering Users
Now that the server is running we can create our first user.\
In terminal run the commands replacing variables where needed.\
Linux:
```
curl --location 'http://YOUR_SERVER_IP:8009/register' \
--header 'Content-Type: application/json' \
--data '{
    "name": "MY_USER",
    "password": "SUPER_SECRET_PASSWORD"
}'
```

Windows-Powershell:
```
$headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
$headers.Add("Content-Type", "application/json")

$body = @"
{
    `"name`": `"MY_USER`",
    `"password`": `"SUPER_SECRET_PASSWORD`"
}
"@

$response = Invoke-RestMethod 'http://YOUR_SERVER_IP:8009/register' -Method 'POST' -Headers $headers -Body $body
$response | ConvertTo-Json

```
You should see a result such as this:
```
{
    "message": "USERNAME registered successfully"
}
```
## Using the API

To fetch data you will need a token\
Add your username and password as base64 encoded string to the command:
```
curl --location --request POST 'http://YOUR_SERVER_IP:8009/login' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic YOUR_ENCODED_STRING'
```
This will return a token.
```
{
    "expiry": "expiry_datetime_as_string",
    "token": "TOKEN"
}
```
You can test the token by:
```
curl --location 'http://YOUR_SERVER_IP:8009/test' \
--header 'Authorization: Bearer TOKEN_FROM_AUTH_HERE'
```
This should return:
```
{
    "message": "test succeeded"
}
```
### Getting Data
Using the token from before, we can now get data from your mqtt.\
Perform a GET request as follows:
```
curl --location --request GET 'http://YOUR_SERVER_IP:8009/sub' \
--header 'Authorization: Bearer TOKEN_FROM_AUTH_HERE \
--data '{
	"mqtt-topic": "mqtt/topic/you/want"
         }'
```

returns:
```
{
    "result": "MESSAGE_AS_STRING"
}
```
### Sending Data
We can now post to the MQTT with retain to true or false by doing the following:
```
curl --location 'http://YOUR_SERVER_IP:8009/pub' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer TOKEN_FROM_AUTH_HERE' \
--data-raw '{
    "mqtt-topic":"mqtt/topic/you/want",
    "mqtt-msg":"DATA_TO_PUBLISH",
    "mqtt-retain":"false"
}'
```