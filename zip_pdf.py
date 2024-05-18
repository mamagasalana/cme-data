import zipfile
from upload_to_drive import GoogleDrive
import os
import glob
import re

gd = GoogleDrive()

def myzip(datelist=None):
    if datelist is None:
        datelistpre  = sorted(set([re.findall('\d{8}', fname)[0]  for fname in glob.glob('*STLBASICPLS*')]))
        datelist = []
        for dt in datelistpre:
            cnt = len(glob.glob(f'{dt}*STLBASICPLS*'))
            if cnt != 27:
                print(f'{dt} does not have 27 files, please verify')
                continue

            if os.path.exists(f'{dt}_files.zip'):
                continue

            datelist.append(dt)

    for dt in datelist:
        file_pattern = dt + '*.txt'
        files_to_zip = glob.glob(file_pattern)
        
        if len(files_to_zip) == 0:
            continue

        # Define the name of the zip file
        zip_filename = f'{dt}_files.zip'

        # Create a zip file and add the files to it
        with zipfile.ZipFile(zip_filename, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
            for file in files_to_zip:
                zipf.write(file)
        print('uploading file to google drive %s' % zip_filename)
        gd.upload_basic(zip_filename)

if __name__ == '__main__':
    import datetime

    myzip()