from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log

class s3fsRemount(ClusterSetup):
    def __init__(self, aws_access_key, aws_secret_key):
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key

    def run(self, nodes, master, user, user_shell, volumes):
        log.info('Mounting S3 bucket')
        master.ssh.execute('s3fs staphopia-samples /mnt/s3/staphopia-samples -o allow_other')
