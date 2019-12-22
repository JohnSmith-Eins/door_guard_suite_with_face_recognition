import paramiko

trans = paramiko.Transport('49.235.10.60', 22)
trans.start_client()
trans.auth_password(username='hgf', password='12345hgf')

sftp = paramiko.SFTPClient.from_transport(trans)
sftp.put('wug.jpg', '/home/hgf/yizhong.jpg')

trans.close()