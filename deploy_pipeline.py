from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log


class DeployPipeline(ClusterSetup):
    def run(self, nodes, master, user, user_shell, volumes):
        for node in nodes:
            log.info("Copying analysis-pipeline to /mnt.")
            node.ssh.execute('cp -r /staphopia/ebs/analysis-pipeline /mnt')

    def on_add_node(self, node, nodes, master, user, user_shell, volumes):
        log.info("Copying analysis-pipeline to /mnt.")
        node.ssh.execute('cp -r /staphopia/ebs/analysis-pipeline /mnt')
