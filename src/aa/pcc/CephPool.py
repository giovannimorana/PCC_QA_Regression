import re
import time
import json
import ast

from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.BuiltIn import RobotNotRunningError

from platina_sdk import pcc_api as pcc
from aa.common import PccUtility as easy

from aa.common.Utils import banner, trace, pretty_print
from aa.common.Result import get_response_data
from aa.common.AaBase import AaBase
from aa.common.Cli import cli_run

PCCSERVER_TIMEOUT = 60 * 3

class CephPool(AaBase):

    def __init__(self):

        # Robot arguments definitions
        self.id = None
        self.ceph_cluster_id = None
        self.name = ""
        self.size = None
        self.tags =  []
        self.pool_type = ""
        self.quota = None
        self.quota_unit = ""
        self.user=""
        self.password=""
        self.nodes_ip=[]
        self.count=0
        super().__init__()

    ###########################################################################
    @keyword(name="PCC.Ceph Get Pool Id")
    ###########################################################################
    def get_ceph_pool_id_by_name(self,*args,**kwargs):
        self._load_kwargs(kwargs)
        pool_id= None
        banner("PCC.Ceph Get Pool Id")

        try:
            conn = BuiltIn().get_variable_value("${PCC_CONN}")
        except Exception as e:
            raise e

        pool_id = easy.get_ceph_pool_id_by_name(conn,self.name)
        return pool_id

    ###########################################################################
    @keyword(name="PCC.Ceph Get All Pools Data")
    ###########################################################################
    def get_ceph_all_pools_data(self,*args,**kwargs):
        self._load_kwargs(kwargs)
        pool_id= None
        banner("PCC.Ceph Get All Pool Data")

        try:
            conn = BuiltIn().get_variable_value("${PCC_CONN}")
        except Exception as e:
            raise e

        response = get_response_data(pcc.get_ceph_pools(conn))
        return response

    ###########################################################################
    @keyword(name="PCC.Ceph Delete All Pools")
    ###########################################################################
    def delete_all_pools(self,*args,**kwargs):
        self._load_kwargs(kwargs)
        banner("PCC.Ceph Delete All Pool")

        try:
            conn = BuiltIn().get_variable_value("${PCC_CONN}")
        except Exception as e:
            raise e

        response = pcc.get_ceph_pools(conn)
        for data in get_response_data(response):
            response=pcc.delete_ceph_pool_by_id(conn,str(data['id']))
            status=self.wait_until_pool_deleted(id=data['id'])
            if status!="OK":
                print("{} deletion failed".format(data['name']))
                return "Error"
        return "OK"

    ###########################################################################
    @keyword(name="PCC.Ceph Get Pool Details For FS")
    ###########################################################################
    def get_pool_details_for_fs(self, *args, **kwargs):
        self._load_kwargs(kwargs)
        banner("PCC.Ceph Get Pool Details For FS")

        temp=dict()        

        try:
            conn = BuiltIn().get_variable_value("${PCC_CONN}")
        except Exception as e:
            raise e

        response = pcc.get_ceph_pools(conn)['Result']['Data']
        print("Response:-"+str(response))
        for data in response:
            if str(data['name']) == str(self.name):
                temp["id"] = data["id"]
                temp["name"]= data["name"]
                temp["size"] = data["size"]
                temp["tags"] = []
                temp["ceph_cluster_id"] = data["ceph_cluster_id"]
                temp["pool_type"] = data["pool_type"]
                temp["quota"] = data["quota"]
                temp["quota_unit"] =  data["quota_unit"]
        return temp

    ###########################################################################
    @keyword(name="PCC.Ceph Get Multiple Pool Details For FS")
    ###########################################################################
    def get_multiple_pool_details_for_fs(self, *args, **kwargs):
        self._load_kwargs(kwargs)
        banner("PCC.Ceph Get Pool Details For FS")

        temp=dict()
        temp_list=[]        

        try:
            conn = BuiltIn().get_variable_value("${PCC_CONN}")
        except Exception as e:
            raise e
        
        response = pcc.get_ceph_pools(conn)['Result']['Data']    
        for val in eval(str(self.name)):
            for data in response:
                if str(data['name']) == str(val):
                    temp["id"] = data["id"]
                    temp["name"]= data["name"]
                    temp["size"] = data["size"]
                    temp["tags"] = ["tags"]
                    temp["ceph_cluster_id"] = data["ceph_cluster_id"]
                    temp["pool_type"] = data["pool_type"]
                    temp["quota"] = data["quota"]
                    temp["quota_unit"] =  data["quota_unit"]
            if len(temp)!=0:        
                temp_list.append(temp)
        return temp_list

    ###########################################################################
    @keyword(name="PCC.Ceph Create Pool")
    ###########################################################################
    def add_ceph_pool(self, *args, **kwargs):
        banner("PCC.Ceph Create Pool")
        self._load_kwargs(kwargs)

        if self.size:
            try:
                self.size= ast.literal_eval(str(self.size))
            except ValueError:
                print("Values is None or AlphaNumeric")

        if self.tags:
            self.tags=eval(self.tags)


        payload = {
            "name":self.name,
            "size":self.size,
            "tags":self.tags,
            "ceph_cluster_id":self.ceph_cluster_id,
            "pool_type":self.pool_type,
            "quota":self.quota,
            "quota_unit":self.quota_unit
        }

        print(payload)
        conn = BuiltIn().get_variable_value("${PCC_CONN}")
        return pcc.add_ceph_pool(conn, payload)


    ###########################################################################
    @keyword(name="PCC.Ceph Create Pool Multiple")
    ###########################################################################
    def create_pool_multiple(self, *args, **kwargs):
        banner("PCC.Ceph Create Pool")
        self._load_kwargs(kwargs)

        if self.size:
            try:
                self.size= ast.literal_eval(str(self.size))
            except ValueError:
                print("Values is None or AlphaNumeric")

        if self.tags:
            self.tags=eval(self.tags)

        if self.count:
            self.count=int(self.count)

        name_bkup = self.name
        for i in range(1,self.count+1):
            name=str(name_bkup)+"-"+str(i)
            payload = {
                "name":name,
                "size":self.size,
                "tags":self.tags,
                "ceph_cluster_id":self.ceph_cluster_id,
                "pool_type":self.pool_type,
                "quota":self.quota,
                "quota_unit":self.quota_unit
                }
            print(payload)
            conn = BuiltIn().get_variable_value("${PCC_CONN}")
            if self.count==i:
                return pcc.add_ceph_pool(conn, payload)
            else:
                response=pcc.add_ceph_pool(conn, payload)
                print(response)
                self.name=name
                status=self.wait_until_pool_ready()
            time.sleep(10)

    ###########################################################################
    @keyword(name="PCC.Ceph Delete Pool")
    ###########################################################################
    def delete_ceph_pool_by_id(self, *args, **kwargs):
        banner("PCC.Ceph Delete Pool")
        self._load_kwargs(kwargs)

        if self.id == None:
            return {"Error": "[PCC.Ceph Delete Pool]: Id of the Pool is not specified."}
        try:
            conn = BuiltIn().get_variable_value("${PCC_CONN}")

        except Exception as e:
            raise e
        return pcc.delete_ceph_pool_by_id(conn,str(self.id))


    ###########################################################################
    @keyword(name="PCC.Ceph Wait Until Pool Ready")
    ###########################################################################
    def wait_until_pool_ready(self, *args, **kwargs):
        banner("PCC.Ceph Wait Until Pool Ready")
        self._load_kwargs(kwargs)

        if self.name == None:
            return None
        try:
            conn = BuiltIn().get_variable_value("${PCC_CONN}")
        except Exception as e:
            raise e

        pool_ready = False
        timeout = time.time() + PCCSERVER_TIMEOUT
  
        while pool_ready == False:
            response = pcc.get_ceph_pools(conn)
            for data in get_response_data(response):
                if str(data['name']).lower() == str(self.name).lower():
                    print(str(data))
                    if data['deploy_status'] == "completed":
                        pool_ready = True
                    if data['deploy_status'] == "failed":
                        return "Error"
                    
            if time.time() > timeout:
                raise Exception("[PCC.Ceph Wait Until Pool Ready] Timeout")
            trace("  Waiting until pool : %s is Ready, currently: %s" % (data['name'], data['progressPercentage']))
            time.sleep(5)
        return "OK"


    ###########################################################################
    @keyword(name="PCC.Ceph Wait Until Pool Deleted")
    ###########################################################################
    def wait_until_pool_deleted(self, *args, **kwargs):
        banner("PCC.Ceph Wait Until Pool Deleted")

        self._load_kwargs(kwargs)

        if self.id == None:
            # pool doesn't exist, nothing to wait for
            return "OK"
        try:
            conn = BuiltIn().get_variable_value("${PCC_CONN}")
        except Exception as e:
            raise e

        Id_found_in_list_of_pools = True
        timeout = time.time() + PCCSERVER_TIMEOUT

        while Id_found_in_list_of_pools == True:
            Id_found_in_list_of_pools = False
            response = pcc.get_ceph_pools(conn)
            for pool in get_response_data(response):
                if str(pool['id']) == str(self.id):
                    name = pool["name"]
                    Id_found_in_list_of_pools = True
            if time.time() > timeout:
                raise Exception("[PCC.Wait Until Pool Deleted] Timeout")
            if Id_found_in_list_of_pools:
                trace("Waiting until node: %s is deleted. Timeout in %.1f seconds." % 
                       (name, timeout-time.time()))
                time.sleep(5)
            else:
                trace("Pool deleted!")
        return "OK"

    ###########################################################################
    @keyword(name="PCC.Ceph Pool Verify BE")
    ###########################################################################
    def verify_ceph_pool_be(self, *args, **kwargs):
        ceph_be_cmd="sudo ceph osd lspools"
        banner("PCC.Ceph Pool Verify BE")
        self._load_kwargs(kwargs)

        for ip in self.nodes_ip:
            output=cli_run(ip,self.user,self.password,ceph_be_cmd)
            if re.search(self.name,str(output)):
                continue
            else:
                return None
        return "OK"

    ###########################################################################
    @keyword(name="PCC.Ceph Pool Update")
    ###########################################################################
    def modify_ceph_pool(self, *args, **kwargs):
        self._load_kwargs(kwargs)

        if self.size:
            try:
                self.size= ast.literal_eval(str(self.size))
            except ValueError:
                print("Values is None or AlphaNumeric")

        if self.tags:
            self.tags=eval(self.tags)

        try:
            payload = {
            "id":self.id,
            "name":self.name,
            "size":self.size,
            "tags":self.tags,
            "ceph_cluster_id":self.ceph_cluster_id,
            "pool_type":self.pool_type,
            "quota":self.quota,
            "quota_unit":self.quota_unit
             }

            conn = BuiltIn().get_variable_value("${PCC_CONN}")
            print(str(payload))
        except Exception as e:
            trace("[update_pool] EXCEPTION: %s" % str(e))
            raise Exception(e)

        return pcc.modify_ceph_pool(conn, payload)