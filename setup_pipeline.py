from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log

class SetupPipeline(ClusterSetup):
    def run(self, nodes, master, user, user_shell, volumes):
        for node in nodes:
            log.info("Pulling analysis-pipeline")
            node.ssh.execute('git clone git@bitbucket.org:staphopia/analysis-pipeline.git /mnt/analysis-pipeline')

            log.info("Building packages")
            node.ssh.execute('cd /mnt/analysis-pipeline && make')

            log.info("Giving ownership to staphopia")
            node.ssh.execute('chown -R staphopia /mnt/analysis-pipeline')
            node.ssh.execute('chgrp -R staphopia /mnt/analysis-pipeline')
