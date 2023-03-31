from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import pathlib
#from . import config

BASE_DIR = pathlib.Path(__file__).resolve().parent

#settings = config.get_settings()
ASTRADB_CONNECT_BUNDLE = BASE_DIR / "connect_bundle" / "secure-connect-video-based-learning-platform-2.zip"

ASTRADB_CLIENT_ID= "cIsXkYgvPldmsWiEYaATRwhU"
ASTRADB_CLIENT_SECRET = "KTmZBMNUvax8.EmeQiNNWQehiHLRB8OzGgWog+a+imt7DZrOk1bd+3Dzr2t9AA0-E+Fv5q4D5E8i545tPSxe_CEtAiJDs53FwZsedxubtxyrL8fXPKXyeyrqOafdXWZf"

cloud_config= {
  'secure_connect_bundle': ASTRADB_CONNECT_BUNDLE
}
auth_provider = PlainTextAuthProvider(ASTRADB_CLIENT_ID, ASTRADB_CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

row = session.execute("select release_version from system.local").one()
if row:
  print(row[0])
else:
  print("An error occurred.")