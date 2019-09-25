import os
import gzip
import shutil

print('Installing requirements...')
os.system('pip install -r requirements.txt')

import requests
import zipfile
import zipfile, struct, io
from clint.textui import progress


def download_data(url, zipped_path):
  # Open the url and download the data with progress bars.
  data_stream = requests.get(url, stream=True)

  with open(zipped_path, 'wb') as file1:
    total_length = int(data_stream.headers.get('content-length'))
    for chunk in progress.bar(data_stream.iter_content(chunk_size=1024),
                              expected_size=total_length / 1024 + 1):
      if chunk:
        file1.write(chunk)
        file1.flush()

  # Extract file.
 
  with open(zipped_path, 'rb') as f:
    data = f.read()

  i = data.rindex(b'PK\5\6') + 22
  i += struct.unpack('<H', data[i-2: i])[0]
  if data[i:].strip(b'\0') == b'':
    data = data[:i]
   
  zf = zipfile.ZipFile(io.BytesIO(data))
 
print('Do you want to download all datasets used in the paper (116 MB)? (y/n)')
if input() == 'y':
  download_data('https://github.com/ricsinaruto/website/blob/master/docs/data.zip?raw=true', 'data.zip')

print('Do you want to download all generated responses on the test set by the different models (7 MB)? (y/n)')
if input() == 'y':
  download_data('https://ricsinaruto.github.io/website/docs/responses.zip', 'responses.zip')
