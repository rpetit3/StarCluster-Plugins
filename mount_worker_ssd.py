from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log


class MountSSD(ClusterSetup):
    def run(self, nodes, master, user, user_shell, volumes):
        for node in nodes:
            if node.alias == "master":
                log.info("Master node, not doing anything.")
            else:
                log.info("Formating First Ephemeral Volume.")
                node.ssh.execute('mkfs -t ext4 /dev/xvdaa')

                log.info("Mounting First Ephemeral Volume.")
                node.ssh.execute('mount -t ext4 /dev/xvdaa /mnt')

    def on_add_node(self, node, nodes, master, user, user_shell, volumes):
        if node.alias == "master":
            log.info("Master node, not doing anything.")
        else:
            log.info("Formating First Ephemeral Volume.")
            node.ssh.execute('mkfs -t ext4 /dev/xvdaa')

            log.info("Mounting First Ephemeral Volume.")
            node.ssh.execute('mount -t ext4 /dev/xvdaa /mnt')
