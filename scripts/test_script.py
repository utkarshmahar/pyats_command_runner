"""
"""
# see https://pubhub.devnetcloud.com/media/pyats/docs/aetest/index.html
# for documentation on pyATS test scripts

# optional author information
# (update below with your contact information if needed)
__author__ = "Utkarsh Mahar"
__copyright__ = "Copyright (c) 2019, Cisco Systems Inc."
__contact__ = ["pyats-support-ext@cisco.com"]
__credits__ = ["list", "of", "credit"]
__version__ = 1.0

import logging


from pyats import aetest
from pyats.log.utils import banner
import socket
# create a logger for this module
logger = logging.getLogger(__name__)


class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def testbed_connect(self, testbed, network_devices,commands):
        """
        establishes connection to all your testbed devices.
        """
        # make sure testbed is provided
        assert testbed, "Testbed is not provided!"
        logger.info("Testbed provided!!")
        assert network_devices, "network_devices are not provided"
        #logger.info("network_devices provided="+str(len(network_devices)))

        self.parent.network_devices = network_devices
        self.parent.testbed = testbed
        self.parent.commands = commands
        self.parent.connected_devices = []
        self.parent.not_connected_devices = []      
        final_list = " "  
        for device in network_devices:
            try: 
             logger.info("Connecting to network_devices: "+device)
             ip = str(testbed.devices[device].connections.cli.ip)
             socket.create_connection((ip,"22"),timeout=1) 
             self.parent.testbed.connect(testbed.devices[device], init_exec_commands=[], init_config_commands=[],learn_hostname = True)
             print
             self.parent.connected_devices.append(device) 
            except:
              self.parent.not_connected_devices.append(device)
              final_list = final_list + "\n" + device       
        print("Connection to "+device+" failed")
        self.passed("---------------SSH to Below Devices Failed-------------"+final_list)

    @aetest.subsection
    def setup(self):
        aetest.loop.mark(Devices, uids=self.parent.connected_devices)


class Devices(aetest.Testcase):
    """
    verify whether all cts pac and all cts environment data has been downloaded to the fabric nodes after provisioning
    """

    @aetest.setup
    def setup(self):
        device = self.uid
        device_obj = self.parent.testbed.devices[self.uid]
        aetest.loop.mark(self.show_command,uids=self.parent.commands)


    @aetest.test
    def show_command(self,section):
        """ tests whether cts pacs were uploaded to fabric node """
        logger.info("test check cts pacs are uploaded on fabric node =" + self.uid)
        device_obj = self.parent.testbed.devices[self.uid]
        output = device_obj.execute(section.uid)
        #self.passed(banner(output))


class CommonCleanup(aetest.CommonCleanup):
    """CommonCleanup Section
    Cleans up the code and reports metrics
    """

    # report metrics
    @aetest.subsection
    def subsection_reporting(self):
        pass



if __name__ == "__main__":
    # for stand-alone execution
    import argparse
    from pyats import topology

    parser = argparse.ArgumentParser(description="standalone parser")
    parser.add_argument(
        "--testbed",
        dest="testbed",
        help="testbed YAML file",
        type=topology.loader.load,
        default=None,
    )

    # do the parsing
    args = parser.parse_known_args()[0]

    aetest.main(testbed=args.testbed)
