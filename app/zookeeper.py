import os

from dotenv import load_dotenv
from kazoo.client import KazooClient

load_dotenv()

ZK_HOSTS = (
    os.getenv("ZOOKEEPER_HOST", "zookeeper") + ":" + os.getenv("ZOOKEEPER_PORT", "2181")
)
zk = None
BASE_PATH = "/url_shortener"


def init_zookeeper(retries: int = 10, delay: int = 3):
    global zk
    zk = KazooClient(hosts=ZK_HOSTS)

    for i in range(retries):
        try:
            zk.start(timeout=5)
            print("Connected to Zookeeper at:", ZK_HOSTS)
            zk.ensure_path("/url_shortener")
            print("Zookeeper connected and path ensured")
            return zk
        except Exception as e:
            print(f"Zookeeper connection failed ({i + 1}/{retries}): {e}")
            import time

            time.sleep(delay)
    raise RuntimeError("Failed to connect to Zookeeper after retries")


def close_zookeeper():
    global zk
    if zk.connected:
        zk.stop()
        zk.close()
        print("Zookeeper connection closed")


def get_next_id() -> int:
    """Get sequential ID from ZooKeeper"""
    node_path = zk.create("/url_shortener/id-", b"", sequence=True, makepath=True)
    seq_num = int(node_path.split("-")[-1])
    return seq_num
