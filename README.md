# Mobile device tokens uploader to cutomer.io

## Usage
* Put `config.py` to the same dir as script `upload_devices.py`
* `pip3 install -r requirements.txt`
* `python3 upload_devices.py`
* Enjoy looking progress bar

### Configuration sample
```
FILE = 'tokens.csv'
SITE_ID = '<your token id>'
API_KEY = '<your API key'
LOG_FILE = 'uploader.log'
```

### Data
Data is CSV file with header `user_id,registration_token,operation_system`

Every entrie is logged into the file defined in `LOG_FILE` parameter in config.