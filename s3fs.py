from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log

class s3fsInstaller(ClusterSetup):
    def __init__(self, aws_access_key, aws_secret_key):
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key

    def run(self, nodes, master, user, user_shell, volumes):
        for node in nodes:
            log.info('Mounting S3 bucket')
            node.ssh.execute('s3fs staphopia /staphopia/s3 -o allow_other')

    def on_add_node(self, node, nodes, master, user, user_shell, volumes):
        log.info('Mounting S3 bucket')
        node.ssh.execute('s3fs staphopia /staphopia/s3 -o allow_other')
