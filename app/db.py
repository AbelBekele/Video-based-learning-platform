import pathlib
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine import connection

BASE_DIR = pathlib.Path(__file__).resolve().parent


ASTRADB_CONNECT_BUNDLE = BASE_DIR / "connect_bundle" / "secure-connect-video-based-learning-platform.zip"

ASTRADB_CLIENT_ID= '<<CLIENT ID>>'
ASTRADB_CLIENT_SECRET = '<<CLIENT SECRET>>'

def get_session():
    cloud_config= {
    'secure_connect_bundle': 'connect_bundle/secure-connect-video-based-learning-platform.zip'
    }
    auth_provider = PlainTextAuthProvider('<<CLIENT ID>>', '<<CLIENT SECRET>>')
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()
    connection.register_connection(str(session), session=session)
    connection.set_default_connection(str(session))

    row = session.execute("select release_version from system.local").one()
    if row:
    print(row[0])
    else:
    print("An error occurred.")
    return session