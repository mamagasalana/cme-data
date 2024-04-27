import zipfile
from upload_to_drive import GoogleDrive
import os
import glob

gd = GoogleDrive()

def myzip(datelist):
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

    dt = datetime.datetime(2024, 4,19)
    dt2 = datetime.datetime(2024, 4,25)  
    delta = dt2 - dt
    datelist = [ (dt+datetime.timedelta(days=x)).strftime('%Y%m%d') for x in range(delta.days+1)]
    myzip(datelist)