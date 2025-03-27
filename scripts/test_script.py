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
        self.parent.devices_via_proxy_obj = []
        self.parent.devices_with_no_ssh = " "
        self.parent.not_connected_devices = " "
        self.parent.devices_via_proxy = " " 

        for device in network_devices:
          logger.info("Connecting to network_device: "+device) 
          ip = str(testbed.devices[device].connections.cli.ip)
          ssh_enabled = False
          if 'proxy' in dict(testbed.devices[device].connections.cli) :
             logger.info("Device "+ device + " to be connected via proxy ") 
             self.parent.devices_via_proxy = self.parent.devices_via_proxy + "\n" + device
             self.parent.devices_via_proxy_obj.append(device) 
             logger.info("Connecting to " + device +"proxy") 
             self.parent.testbed.connect(testbed.devices[device], init_exec_commands=[], init_config_commands=[],learn_hostname = True)
             logger.info(str(testbed.devices[device].hostname)) 
             if testbed.devices[device].connected and str(testbed.devices[device].hostname) == device:
              logger.info(f"Connection to {device} via proxy successful") 
              self.parent.connected_devices.append(device)
              testbed.devices[device].disconnect()
              logger.info(f"Connection to {device} via proxy disconnected") 
             else:
              testbed.devices[device].disconnect()
              logger.info(f"Connection to {device} via proxy failed") 
              self.parent.not_connected_devices = self.parent.not_connected_devices + "\n" + device
              logger.info(f"Connection to {device} via proxy failed") 
 
          else:
            logger.info("Connecting to " + device +"without proxy") 
            try:
             socket.create_connection((ip,"22"),timeout=1) 
             logger.info(f"port 22 on device {device} open")
             ssh_enabled = True
            except:
             logger.info(f"port 22 on device {device} closed")
             self.parent.devices_with_no_ssh = self.parent.devices_with_no_ssh + "\n" + device 
          if ssh_enabled:
             logger.info(f"connecting to device {device}")
             self.parent.testbed.connect(testbed.devices[device], init_exec_commands=[], init_config_commands=[],learn_hostname = True)
             if testbed.devices[device].connected:
              logger.info(f"SSH to device {device} was successful")  
              self.parent.connected_devices.append(device) 
             else:
               logger.info(f"SSH to device {device} failed") 
               self.parent.not_connected_devices = self.parent.not_connected_devices + "\n" + device

     
        logger.info("---------------No port 22 enabled on below devices-------------"+self.parent.devices_with_no_ssh)
        logger.info("---------------SSH to Below Devices Failed-------------"+self.parent.not_connected_devices)
        logger.info("---------------SSH to Below Devices Require proxy-------------" + self.parent.devices_via_proxy)
        
    @aetest.subsection
    def setup(self):
        logger.info(self.parent.connected_devices)
        aetest.loop.mark(Devices, uids=(self.parent.connected_devices))
       


class Devices(aetest.Testcase):
    

    @aetest.setup
    def setup(self):
        device = self.uid
        device_obj = self.parent.testbed.devices[self.uid]
        if device_obj.connected: 
         logger.info(device+ "in connected mode")
         aetest.loop.mark(self.show_command,uids=self.parent.commands)
        else:
            logger.info(f"{device} in diconnected mode")
            logger.info("connecting again")
            device_obj.connect(init_exec_commands=[], init_config_commands=[],learn_hostname = True)
            aetest.loop.mark(self.show_command,uids=self.parent.commands)
         
    @aetest.test
    def show_command(self,section):
    
        logger.info("Applying command " + section.uid)
        device_obj = self.parent.testbed.devices[self.uid]
        output = device_obj.execute(section.uid)
        #self.passed(banner(output))

    @aetest.cleanup
    def disconnect(self):
        
        logger.info("Disconnecting " )
        self.parent.testbed.devices[self.uid].disconnect()  


class CommonCleanup(aetest.CommonCleanup):
    """CommonCleanup Section
    Cleans up the code and reports metrics
    """

    # report metrics
    @aetest.subsection
    def subsection_reporting(self):
          
        logger.info("---------------No port 22 enabled on below devices-------------"+self.parent.devices_with_no_ssh)
        logger.info("---------------SSH to Below Devices Failed-------------"+self.parent.not_connected_devices)
        logger.info("---------------SSH to Below Devices Require proxy-------------" + self.parent.devices_via_proxy)
        



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
