from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log

class UbuntuUpgrader(ClusterSetup):
    def run(self, nodes, master, user, user_shell, volumes):
        log.info("Updating the system on master node")
        master.ssh.execute('apt-get -y update')
        master.ssh.execute('DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade')
        master.ssh.execute('apt-get -y autoremove')
