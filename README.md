# Create the backup of website files and store at the remote backup server 

The below code can backup the files from a user specified directory to a user specified tar.gz file in a preferred location using python code. 

## Tasks
- List the directories which need to take the backup. 
- Find out the absolute path of the directories
- Create the time stamp and tar.gz file within the specified directory
- Change the absolute path of the directory and copy the content
- Creating an sftp server
- Creating paysft connection
- Upload the backup file to the remote backup server and remove the same from the source server.


### List the directories which need to take the backup.

  Here I am going take list the direcory to take the backup under the directory /htdocs.
  
  ```python
  import os

documentroot = '/htdocs'
for directory in os.listdir(documentroot):
    print(directory)
```

 ### Result  
 
 ```bash
ubuntu@/:~$ python3 listdirectory.py
zerocover.net
landmark.com
ubuntu@/:~$
```

### Find out the absolute path of the directories

```python
import os

documentroot = '/htdocs'
for directory in os.listdir(documentroot):
   abspath = os.path.join(documentroot,directory)

   print(abspath)
```
### Result

```bash
ubuntu@/:~$ python3  absolutepath.py
/htdocs/zerocover.net
/htdocs/landmark.com
```
### Create the time stamp and tar.gz file within the specified directory
  
The backup file is stored with the creating time. Here I am creating timestamp with the format date-month-year-minute-hour and 
place the directory in the /tmp/backup/ folder.
To create a timestamp and tar file, we need to initialize the module datetime and tarfile.
  
  ```python
  import os
import datetime
import tarfile

documentroot = '/htdocs'
for directory in os.listdir(documentroot):

        objectmethod = datetime.datetime.now()
        abspath = os.path.join(documentroot,directory)
        timestamp = '{}-{}-{}-{}-{}'.format(objectmethod.day,objectmethod.month,objectmethod.year,objectmethod.hour,objectmethod.minute)
        filename = '/tmp/backup/{}-{}.tar.gz'.format(directory,timestamp)


        with tarfile.open(filename,'w:gz') as tar:
            print(tar)
```

### Result

```
ubuntu@/:/tmp/backup$ pwd
/tmp/backup
ubuntu@/:/tmp/backup$ ll
total 20
-rw-rw-r--  1 ubuntu ubuntu   77 Aug 15 06:57 landmark.com-15-8-2019-6-57.tar.gz
-rw-rw-r--  1 ubuntu ubuntu   78 Aug 15 06:57 zerocover.net-15-8-2019-6-57.tar.gz
ubuntu@/:/tmp/backup$ du -sch landmark.com-15-8-2019-6-57.tar.gz
4.0K    landmark.com-15-8-2019-6-57.tar.gz
4.0K    total
```

### Change the absolute path of the directory and copy the content
Here I am going to change the absolute path of the directory the current location of the files and copy all content to the backup file.

```python
import os
import datetime
import tarfile

documentroot = '/htdocs'
for directory in os.listdir(documentroot):

        objectmethod = datetime.datetime.now()
        abspath = os.path.join(documentroot,directory)
        timestamp = '{}-{}-{}-{}-{}'.format(objectmethod.day,objectmethod.month,objectmethod.year,objectmethod.hour,objectmethod.minute)
        filename = '/tmp/backup/{}-{}.tar.gz'.format(directory,timestamp)


        with tarfile.open(filename,'w:gz') as tar:
            os.chdir(abspath)
            tar.add('.')
```

### Result

```bash
ubuntu@/:/tmp/backup$ ll
total 21704
-rw-rw-r--  1 ubuntu ubuntu      532 Aug 15 07:08 backup.py
-rw-rw-r--  1 ubuntu ubuntu 11098489 Aug 15 07:09 landmark.com-15-8-2019-7-9.tar.gz
-rw-rw-r--  1 ubuntu ubuntu 11111050 Aug 15 07:09 zerocover.net-15-8-2019-7-9.tar.gz
ubuntu@/:/tmp/backup$ du -sch landmark.com-15-8-2019-7-9.tar.gz
11M     landmark.com-15-8-2019-7-9.tar.gz
11M     total
```

### Creating sftp server

You can create the FTP user at the remote backup server with the password authentication privillage.
```bash
sudo useradd sftpuser 

$ sudo passwd sftpuser


Changing password for user sftpuser.
New password: 
Retype new password: 
passwd: all authentication tokens updated successfully.
 
 sudo vim /etc/ssh/sshd_config

# To disable tunneled clear text passwords, change to no here!
PasswordAuthentication yes
#PermitEmptyPasswords no
#PasswordAuthentication no
 ```
### Creating pysftp connection

```
import pysftp


sftp_user = 'sftpuser'
sftp_password = 'clado123'
sftp_host = '172.31.21.199'
sftp_port = 22

sftp = pysftp.Connection(username=sftp_user,port=sftp_port,host=sftp_host,password=sftp_password)
sftp.put('/tmp/backupname')
sftp.close()
```
### Upload the backup file to the remote backup server and remove the same from the source server

```python
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
```
### Result

```bash
[sftpuser@/ ~]$ ll
total 21692
-rw-rw-r-- 1 sftpuser sftpuser 11098489 Aug 15 08:04 landmark.com-15-8-2019-8-4.tar.gz
-rw-rw-r-- 1 sftpuser sftpuser 11111050 Aug 15 08:04 zerocover.net-15-8-2019-8-4.tar.gz
[sftpuser@/ ~]$
```

