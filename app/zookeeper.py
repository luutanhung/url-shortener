from kazoo.client import KazooClient
from kazoo.handlers.threading import KazooTimeoutError

ZK_HOSTS = "127.0.0.1:2181"
zk = None
BASE_PATH = "/url_shortener"


def init_zookeeper():
    global zk
    zk = KazooClient(hosts=ZK_HOSTS)

    try:
        zk.start(timeout=5)
        zk.ensure_path("/url_shortener")
        print("Zookeeper connected and path ensured")
    except KazooTimeoutError:
        print("Failed to connect to Zookeeper within timeout")
        raise


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
