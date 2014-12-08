from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log

class s3fsInstaller(ClusterSetup):
    def __init__(self, aws_access_key, aws_secret_key):
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key

    def run(self, nodes, master, user, user_shell, volumes):
        log.info("Installing required packages")
        master.ssh.execute('apt-get -y update')
        master.ssh.execute('apt-get -y install libfuse-dev fuse-utils libcurl4-openssl-dev libxml2-dev libtool')

        log.info('Installing s3fs-fuse')
        master.ssh.execute('git clone https://github.com/s3fs-fuse/s3fs-fuse /tmp/s3fs')
        master.ssh.execute('cd /tmp/s3fs && ./autogen.sh')
        master.ssh.execute('cd /tmp/s3fs && ./configure --prefix=/usr --with-openssl')
        master.ssh.execute('cd /tmp/s3fs && make')
        master.ssh.execute('cd /tmp/s3fs && make install')

        log.info('Mounting S3 bucket')
        master.ssh.execute('mkdir -p /mnt/s3/staphopia-samples')
        master.ssh.execute("echo '{0}:{1}' > /etc/passwd-s3fs".format(self.aws_access_key, self.aws_secret_key))
        master.ssh.execute('chmod 640 /etc/passwd-s3fs')
        master.ssh.execute('s3fs staphopia-samples /mnt/s3/staphopia-samples -o allow_other')
