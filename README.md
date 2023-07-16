# measurement-server

Server for temperature meausuring API, hardware remote settings and monitoring.

Requirements: 
- Python 3.10
- pip

Install all dependencies:
```pip install -r requirements.txt```

Run Uvicorn Server:
```uvicorn main:app```

In my case, it's:
```uvicorn main:app --host 0.0.0.0 --port 80```

Go to URL:
```http://127.0.0.1```

Enjoy!



# Docs

Docs for the most of the endpoints is:
```/docs```


## Additional docs for Websocket Endpoints:

**IT HAS THE SAME PORT AS YOUR SERVER AT**

Websockets are used to listen for some events:



```/api/ws/settings```
You can listen for settings changes with it. Will be used in Arduino sometime...

The model of the messages are:

```json
{
    "event": "setting_changed",
    "setting_key": "ssid",
    "setting_value": "my awesome wifi"
}
```
```json
{
    "event": "setting_changed",
    "setting_key": "password",
    "setting_value": "Pa$$w0rd"
}
```
```json
{
    "event": "setting_changed",
    "setting_key": "pseudo_table_id",
    "setting_value": "mytable123" #the table is that the data is need to put into
}
```