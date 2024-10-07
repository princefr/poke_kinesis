## Kirin destineo Kinesis poke

Repository for storing the Kinesis poke for kirin.
It contains: KinesisRecord, Shard and StreamDescription models representing actual Kinesis Data model as python class

## Usage

1. To get started, please first install the requirements

```
  pip3 install -r requirements.txt
```

2. Please update  your ~/.aws/credentials to add the installation credentials.
   Credentials can be found in your aws console https://navitia.awsapps.com/start/#/?tab=accounts


```
[blablablabla_DevOpsAccess]
aws_access_key_id=""
aws_secret_access_key=""
aws_session_token=""
```
  * You can manage AWS authentification as you please.


3. Please update the main.py with your informations.

```
os.environ['AWS_PROFILE'] = ""
STREAM_NAME=""
REGION_NAME="eu-west-1"
```


4. You can now run the main.py file

```
python3 main.py
```
