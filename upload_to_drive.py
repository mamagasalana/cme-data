# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 21:07:45 2023

@author: ASUS
"""

from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import time

# https://cloud.google.com/docs/authentication/provide-credentials-adc

FOLDER_ID = [{'id': '1KFarKxPorLKImRdwzitWmfaYrQ5kgEX0'}]
API_KEY = 'AIzaSyBNiKqj3iYTNJrUDSg1-0G-YoHVOPvpG4Y' # get from API->Credentials page in console.cloud.googl.com
SCOPES = ['https://www.googleapis.com/auth/drive']

class GoogleDrive:
    def __init__(self):
        creds, _ = google.auth.load_credentials_from_file('credentials.json', scopes=SCOPES)
        # create drive api client
        self.service = build('drive', 'v2', credentials=creds)

    def upload_basic(self, filename : str):
        """Insert new file.
        Returns : Id's of the file uploaded
        """
        for _ in range(5):
            try:
                file_metadata = {'title': filename, 
                                'parents': FOLDER_ID }
                media = MediaFileUpload(filename, mimetype='text/csv')
                file = self.service.files().insert(body=file_metadata,  media_body=media, fields='id').execute()
                
                print(f'File ID: {file.get("id")}')
                return file.get('id')
            
            except Exception as e:
                e2 = e
                print('Retrying ...')
                pass
            
            time.sleep(5)
            
        print(f'An error occurred: {str(e2)}')
        file = None
        return
