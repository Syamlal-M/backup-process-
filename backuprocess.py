import os
import datetime
import tarfile
import pysftp

sftp_user = 'sftpuser'
sftp_password = 'root123'
sftp_host = '13.127.110.198'
sftp_port = 22
documentroot = '/htdocs'

documentroot = '/htdocs'
def upload(archiveName):

    with pysftp.Connection(username=sftp_user,port=sftp_port,host=sftp_host,password=sftp_password) as sftp:

        sftp.put(archiveName)
for directory in os.listdir(documentroot):

        objectmethod = datetime.datetime.now()
        abspath = os.path.join(documentroot,directory)
        timestamp = '{}-{}-{}-{}-{}'.format(objectmethod.day,objectmethod.month,objectmethod.year,objectmethod.hour,objectmethod.minute)
        filename = '/tmp/backup/{}-{}.tar.gz'.format(directory,timestamp)


        with tarfile.open(filename,'w:gz') as tar:
            os.chdir(abspath)
            tar.add('.')

        upload(filename)
        os.remove(filename)

