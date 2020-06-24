import time
import os
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.BuiltIn import RobotNotRunningError
from platina_sdk import pcc_api as pcc
from aa.common import PccUtility as easy
from aa.common.Utils import banner, trace, pretty_print
from aa.common.Result import get_response_data, get_result
from aa.common.AaBase import AaBase
from aa.common.Cli import *

class Cli(AaBase):
    """ 
    Cli
    """

    def __init__(self):
        self.cmd = None
        self.host_ip = None
        self.linux_password = None
        self.linux_user = None
        self.remote_source = None
        self.local_destination = None
        super().__init__()

    ###########################################################################
    @keyword(name="CLI.Run")
    ###########################################################################
    def cli_run(self, *args, **kwargs):
        """
        CLI Run
        [Args]
            (str) cmd: 
            (str) host_ip:
            (str) linux_password:
            (str) linux_user:
        [Returns]
            (dict) Response: CLI Run response
        """
        self._load_kwargs(kwargs)
        banner("CLI.Run ip=%s [cmd=%s]" % (self.host_ip, self.cmd))
        return cli_run(self.host_ip, self.linux_user, self.linux_password, self.cmd)

    ###########################################################################
    @keyword(name="CLI.Truncate PCC Logs")
    ###########################################################################
    def cli_truncate_pcc_logs(self, *args, **kwargs):
        """
        CLI Truncate PCC Logs
        [Args]
            (str) host_ip:
            (str) linux_password:
            (str) linux_user:
        [Returns]
            (str) OK if command successful, stderr output if there's an error
        """
        self._load_kwargs(kwargs)
        print("kwargs"+str(kwargs))
        banner("CLI.Truncate PCC Logs ip=%s" % self.host_ip)
        ret = cli_truncate_pcc_logs(self.host_ip, self.linux_user, self.linux_password)
        print("Response"+str(ret))
        if ret.stderr == "":
            return "OK"
        else:
            return ret.stderr


    ###########################################################################
    @keyword(name="CLI.Copy PCC Logs")
    ###########################################################################
    def cli_copy_pcc_logs(self, *args, **kwargs):
        """
        CLI Copy+ PCC Logs
        [Args]
            (str) host_ip:
            (str) linux_password:
            (str) linux_user:
            (str) remote_source
            (str) local_destination

        [Returns]
            (str) OK if command successful, stderr output if there's an error
        """
        self._load_kwargs(kwargs)
        print("kwargs:-"+str(kwargs))
        banner("CLI.Copy PCC Logs ip=%s" % self.host_ip)
        return cli_copy_pcc_logs(self.host_ip, self.linux_user, self.linux_password)