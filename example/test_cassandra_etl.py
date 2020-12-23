from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

'''
cloud_config = {
    'secure_connect_bundle': '/path/to/secure-connect-dbname.zip'
}
'''

auth_provider = PlainTextAuthProvider(username='database', password='123456')
#cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
#session = cluster.connect()

#cluster = Cluster(['localhost'], port=34)
cluster = Cluster(['localhost'], port=34, auth_provider=auth_provider )

#set keyspace
#session = cluster.connect('jimbo')
session = cluster.connect('facebook')

#query from table
#print(session.execute("SELECT * FROM jimbo.users").one())
print(session.execute("SELECT * FROM facebook.posts").one())