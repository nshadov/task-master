# Task-master

Sample queue created based on AWS DynamoDB that could be deployed as AWS Lambda.

## Configure

You could deploy this function using AWS Lambda. Make sure to review ```zappa_settings.json```, add
keys for user that could be able to read/write/create table on AWS DynamoDB. Then deploy your code:

```
zappa deploy
```

## Run

You could run project locally (it's using python Flask) using:

```
./main.py
```

or

```
python -m flask ./main.py
```

## API

Review API documentation by browing ```http[s]://<YOUR_URL>/help```.