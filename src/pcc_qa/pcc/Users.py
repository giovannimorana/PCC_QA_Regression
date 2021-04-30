import time
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.BuiltIn import RobotNotRunningError

from platina_sdk import pcc_api as pcc
from pcc_qa.common import PccUtility as easy

from pcc_qa.common.Utils import banner, trace, pretty_print
from pcc_qa.common.Result import get_response_data, get_result
from pcc_qa.common.PccBase import PccBase

class Users(PccBase):
    """ 
    Users
    """

    def __init__(self):
        self.Username = None
        self.Tenant = None
        self.FirstName = None
        self.LastName = None
        self.Email = None
        self.Role_ID =None
        self.Active = None
        self.Token = None
        self.Password = None
        self.Source = None
        super().__init__()

        '''
        {"username": "anurag.jain@calsoftinc.com", "tenant": 4, "firstname": "Anurag", "lastname": "jain",
         "email": "anurag.jain@calsoftinc.com", "roleID": 8, "active": true,
         "source": "https://172.17.2.218:9999/gui/setPass", "protect": false}
        '''
    ###########################################################################
    @keyword(name="PCC.Add User")
    ###########################################################################
    def add_user(self, *args, **kwargs):
        """
        Add User
        """
        self._load_kwargs(kwargs)
        print("Kwargs are:{}".format(kwargs))
        banner("PCC.Add User [Name=%s]" % self.Username)
        conn = BuiltIn().get_variable_value("${PCC_CONN}")
        print("conn is {}".format(conn))

        '''
        
        {"firstname": "calsoft","lastname": "platina","username": "calsoftplatina@gmail.com",
        "email": "calsoftplatina@gmail.com", "roleID": 74,"tenant": 77,"active": true}
        
        payload = {
            "firstname": self.FirstName,
            "lastname": self.LastName,
            "username": self.Username,
            "email": self.Username,
            "roleID": self.Role_ID,
            "tenant": self.Tenant,
            "active": "true",
            "source":"https://172.17.3.226:9999/gui/setPass"
        }
        
        Source=${PCC_URL}
        self.Source
        '''
        pcc_source = self.Source + "/gui/setPass"
        payload = {
            "firstname": self.FirstName,
            "lastname": self.LastName,
            "username": self.Username,
            "email": self.Username,
            "roleID": self.Role_ID,
            "tenant": self.Tenant,
            "active": "true",
            "source": pcc_source
        }
        print("payload is {}".format(payload))
        return pcc.add_user(conn,payload)

    ###########################################################################
    @keyword(name="PCC.Delete User")
    ###########################################################################
    def delete_user(self, *args, **kwargs):
        """
        Delete User
        """
        self._load_kwargs(kwargs)
        print("Kwargs are:{}".format(kwargs))
        banner("PCC.Delete User [Name=%s]" % self.Username)
        conn = BuiltIn().get_variable_value("${PCC_CONN}")
        print("conn is {}".format(conn))

        payload = {
            "username": self.Username
        }
        print("payload is {}".format(payload))
        return pcc.delete_user(conn,data = payload)

    ###########################################################################
    @keyword(name="PCC.Create User Password")
    ###########################################################################
    def create_user_password(self, *args, **kwargs):
        """
        Create User Password
        """
        self._load_kwargs(kwargs)
        print("Kwargs are:{}".format(kwargs))

        '''
        {'session': <requests.sessions.Session object at 0x7f776ea29438>, 
        'token': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTYxOTQzMTgwOSwiaWF0IjoxNjE4ODI3MDA5fQ.8s9mmyLKhTMk8PIqk4jDCiFtV7QqOFLxH0nNwhpIYRnAWrq7CCvh_a3WhRUP_AU2P7WzE_fsBLmxzc-aJfCQJA', 
        'url': 'https://172.17.3.226:9999', 'proxies': {}, 'options': {'insecure': False, 'use_session': True}}
        '''



        banner("PCC.Add User [password=%s]" % self.Password)
        token = BuiltIn().get_variable_value("${password_token}")
        print("token is {}".format(token))
        conn = BuiltIn().get_variable_value("${PCC_CONN}")
        print("conn is {}".format(conn))
        conn["token"] = token
        print("updated conn= {}".format(conn))
        payload = {"password": self.Password}
        print("payload is {}".format(payload))


        return pcc.add_user_password(conn,payload)
