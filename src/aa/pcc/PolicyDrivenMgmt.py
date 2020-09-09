import time
import re
import os
import json
import ast

from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.BuiltIn import RobotNotRunningError
from robot.api import logger

from platina_sdk import pcc_api as pcc
from aa.common import PccUtility as easy

from aa.common.Utils import banner, trace, pretty_print
from aa.common.Result import get_response_data
from aa.common.AaBase import AaBase
from aa.common.Cli import cli_run
from aa.pcc.Nodes import Nodes

PCCSERVER_TIMEOUT = 60*40
PCCSERVER_TIMEOUT_UPGRADE = 60*60


class PolicyDrivenMgmt(AaBase):
    
    def __init__(self):
        # Robot arguments definitions
        self.Id= None
        self.Name=None
        self.type = None
        self.scope_name = None
        self.description = None
        self.parentID = None
        self.appId = None
        self.app_name = None
        self.node_name = None
        self.node_role_name = None
        self.scopeIds = []
        self.scopeId= None
        self.inputs = []
        self.owner = 0
        self.policyID = None
        self.policyIDs = []
        self.node_names = []
        self.targetNodeIp = []
        self.user="pcc"
        self.password="cals0ft"
        self.roles_id = None
        super().__init__()

    ###########################################################################
    @keyword(name="PCC.Get All Scopes")
    ###########################################################################
    def get_all_scopes(self,*args,**kwargs):
        self._load_kwargs(kwargs)
        banner("PCC.Get All Scopes")
        try:
            conn = BuiltIn().get_variable_value("${PCC_CONN}")
        except Exception as e:
            raise e

        response = pcc.get_all_scopes(conn)
        return response
        
    ###########################################################################
    @keyword(name="PCC.Get Scope Types")
    ###########################################################################
    def get_scope_types(self,*args,**kwargs):
        self._load_kwargs(kwargs)
        banner("PCC.Get Scope Types")
        try:
            conn = BuiltIn().get_variable_value("${PCC_CONN}")
        except Exception as e:
            raise e

        response = pcc.get_scope_types(conn)
        return response

    ###########################################################################
    @keyword(name="PCC.Get Scope Details")
    ###########################################################################
    def get_scope_details(self,*args,**kwargs):
        self._load_kwargs(kwargs)
        banner("PCC.Get Scope Details")
        try:
            conn = BuiltIn().get_variable_value("${PCC_CONN}")
            Id = easy.get_scope_id_by_name(conn, Name=self.scope_name, ParentID=self.parentID)
        except Exception as e:
            return "Error in get_scope_details: {}".format(e)

        response = pcc.get_scope(conn,id=str(Id))
        return response

    ###########################################################################
    @keyword(name="PCC.Create Scope")
    ###########################################################################
    def add_scope(self, *args, **kwargs):
        banner("PCC.Create Scope")
        self._load_kwargs(kwargs)
        conn = BuiltIn().get_variable_value("${PCC_CONN}")        
        print("ParentID is {} and type is {}".format(self.parentID, type(self.parentID)))
        if self.parentID:
            payload = {
                "type": self.type,
                "name": self.scope_name,
                "description": self.description,
                "parentID":self.parentID,
                "policyIDs":self.policyIDs
                }
        else:
            payload = {
                "type": self.type,
                "name": self.scope_name,
                "description": self.description,
                "policyIDs":self.policyIDs
                }
       
        print("payload:-"+str(payload)) 
        return pcc.add_scope(conn, payload)
        
    ###########################################################################
    @keyword(name="PCC.Check Scope Creation From PCC")
    ###########################################################################
    def check_scope_creation(self, *args, **kwargs):
        banner("PCC.Check Scope Creation From PCC")
        self._load_kwargs(kwargs)
        conn = BuiltIn().get_variable_value("${PCC_CONN}")        
        scopes = self.get_all_scopes(conn)['Result']['Data']
        scope_search = re.search(self.scope_name,str(scopes))
        if scope_search:
            return "OK"
        return "Scope with name {} not found on PCC".format(self.scope_name)
        
    ###########################################################################
    @keyword(name="PCC.Get Scope Id")
    ###########################################################################
    def get_scope_id(self,*args,**kwargs):
        self._load_kwargs(kwargs)
        banner("PCC.Get Scope Id")
        conn = BuiltIn().get_variable_value("${PCC_CONN}")
        Id = easy.get_scope_id_by_name(conn, Name=self.scope_name, ParentID=self.parentID)
        return Id
    
    ###########################################################################
    @keyword(name="PCC.Update Scope")
    ###########################################################################
    def modify_scope(self, *args, **kwargs):
        banner("PCC.Update Scope")
        self._load_kwargs(kwargs)
        conn = BuiltIn().get_variable_value("${PCC_CONN}")        
        if 'policyIDs' in kwargs:
            self.policyIDs = ast.literal_eval(kwargs['policyIDs'])
        if self.parentID:
            payload = {
                "id":self.Id,
                "type": self.type,
                "name": self.scope_name,
                "description": self.description,
                "parentID":self.parentID,
                "policyIDs":self.policyIDs
                }
        else:
            payload = {
                "id":self.Id,
                "type": self.type,
                "name": self.scope_name,
                "description": self.description,
                "policyIDs":self.policyIDs
                }
       
        print("payload:-"+str(payload)) 
        return pcc.modify_scope_by_id(conn, id=str(self.Id), data=payload)
        
    
    ###########################################################################
    @keyword(name="PCC.Delete Scope")
    ###########################################################################
    
    def delete_scope(self, *args, **kwargs):
        banner("PCC.Delete Scope")
        self._load_kwargs(kwargs)
        conn = BuiltIn().get_variable_value("${PCC_CONN}")
        
        Id = easy.get_scope_id_by_name(conn, Name=self.scope_name, ParentID=self.parentID)
        return pcc.delete_scope_by_id(conn, str(Id))
        
    ###########################################################################
    @keyword(name="PCC.Apply Policy To Scope")
    ###########################################################################
    
    def apply_policy(self, *args, **kwargs):
        banner("PCC.Apply Policy To Scope")
        self._load_kwargs(kwargs)
        conn = BuiltIn().get_variable_value("${PCC_CONN}")
        payload= {}
        
        Id = easy.get_scope_id_by_name(conn, Name=self.scope_name, ParentID=self.parentID)
        return pcc.apply_policy(conn, str(Id), data=payload)
        
    
    ###########################################################################
    @keyword(name="PCC.Get All Policies")
    ###########################################################################
    def get_all_policies(self,*args,**kwargs):
        self._load_kwargs(kwargs)
        banner("PCC.Get All Policies")
        conn = BuiltIn().get_variable_value("${PCC_CONN}")
        response = pcc.get_all_policies(conn)
        return response
    
    ###########################################################################
    @keyword(name="PCC.Get Policy Inputs from Apps")
    ###########################################################################
    def get_policy_inputs_from_apps(self,*args,**kwargs):
        self._load_kwargs(kwargs)
        banner("PCC.Get Policy Inputs from Apps")
        try:
            conn = BuiltIn().get_variable_value("${PCC_CONN}")
            print("kwargs in get_policy_inputs_from_apps are : {}".format(kwargs))
            data = pcc.get_policy_enabled_apps(conn)['Result']['Data']
            for i in data:
                if self.Name.lower() in i.values():
                    values= i['actions'][0]['inputs']
            required_data = []
            for val in values:
                internal_dict = {}
                internal_dict.update(name= val['name'], value=val['default'])
                required_data.append(internal_dict)
        except Exception as e:
            return "Error in get_policy_inputs_from_apps: {}".format(e)

        return required_data
        
    ###########################################################################
    @keyword(name="PCC.Get App Id from Policies")
    ###########################################################################
    def get_app_id_from_policies(self,*args,**kwargs):
        self._load_kwargs(kwargs)
        banner("PCC.Get App Id from Policies")
        try:
            conn = BuiltIn().get_variable_value("${PCC_CONN}")
            logger.console("kwargs are : {}".format(kwargs))
            data = pcc.get_policy_enabled_apps(conn)['Result']['Data']
            for i in data:
                if self.Name.lower() in i.values():
                    app_id_from_policy =  i['id']
                    logger.console("app_id_from_policy: {}".format(app_id_from_policy))
        except Exception as e:
            return "Error in get_app_id_from_policies: {}".format(e)
        return app_id_from_policy
           
    ###########################################################################
    @keyword(name="PCC.Get Policy Details")
    ###########################################################################
    def get_policy_details(self,*args,**kwargs):
        self._load_kwargs(kwargs)
        banner("PCC.Get Policy Details")
        try:
            conn = BuiltIn().get_variable_value("${PCC_CONN}")
            print("kwargs are : {}".format(kwargs))
            appId = self.get_app_id_from_policies(conn,Name=self.Name) 
            print("appId is {}".format(appId))
            Id = easy.get_policy_id(conn, Desc=self.description, AppID=appId)
            print("Id fetched is {}".format(Id))
        except Exception as e:
            return "Error in get_policy_details: {}".format(e)

        response = pcc.get_policy(conn,id=str(Id))
        return response
    
    
    
    ###########################################################################
    @keyword(name="PCC.Create Policy")
    ###########################################################################
    def add_policy(self, *args, **kwargs):
        banner("PCC.Create Policy")
        self._load_kwargs(kwargs)
        conn = BuiltIn().get_variable_value("${PCC_CONN}")
        logger.console("Kwargs: {}".format(kwargs))        
        if 'appId' in kwargs:
            if type(kwargs['appId']) == str:
                if kwargs['appId'].isnumeric():
                    self.appId = ast.literal_eval(kwargs['appId'])
                else:
                    self.appId = kwargs['appId']
            else:
                self.appId = int(kwargs['appId'])
        if 'inputs' in kwargs:
            self.inputs = ast.literal_eval(kwargs['inputs'])
        else:
            self.inputs = self.get_policy_inputs_from_apps(kwargs)
            
        if 'scopeIds' in kwargs:
            self.scopeIds =  ast.literal_eval(self.scopeIds)
            
        print("Kwargs in create policy are:{}".format(kwargs))
        print("inputs is :{} and appId is {} and scopeID is {} and description is {}".format(self.inputs,self.appId,self.scopeIds,self.description))
        payload = {
            "appId": self.appId,
            "scopeIDs": self.scopeIds,
            "description": self.description,
            "inputs":self.inputs,
            "owner":self.owner
            }
        
        print("Payload is :{}".format(payload))
       
        logger.console("payload:-"+str(payload)) 
        return pcc.add_policy(conn, payload)
        
    ###########################################################################
    @keyword(name="PCC.Get Policy Id")
    ###########################################################################
    def get_policy_id(self,*args,**kwargs):
        self._load_kwargs(kwargs)
        logger.console("Kwargs are : {}".format(kwargs))
        banner("PCC.Get Policy Id")
        conn = BuiltIn().get_variable_value("${PCC_CONN}")
        appId = self.get_app_id_from_policies(conn,Name=self.Name) 
        logger.console("App id in get policy id is {}".format(appId))
        Id = easy.get_policy_id(conn, Desc=self.description, AppID=appId)
        return Id
    
    
    ###########################################################################
    @keyword(name="PCC.Update Policy")
    ###########################################################################
    def modify_policy(self, *args, **kwargs):
        banner("PCC.Update Policy")
        self._load_kwargs(kwargs)
        print("Kwargs are: {}".format(kwargs))
        conn = BuiltIn().get_variable_value("${PCC_CONN}") 
        if 'appId' in kwargs:
            if type(kwargs['appId']) == str:
                if kwargs['appId'].isnumeric():
                    self.appId = ast.literal_eval(kwargs['appId'])
                else:
                    self.appId = kwargs['appId']
            else:
                self.appId = int(kwargs['appId'])
        if 'inputs' in kwargs:
            self.inputs = ast.literal_eval(kwargs['inputs'])
        else:
            self.inputs = self.get_policy_inputs_from_apps(**kwargs)       
        if 'scopeIds' in kwargs:
            self.scopeIds =  ast.literal_eval(self.scopeIds)
            
        print("self.inputs is {}".format(self.inputs))
        payload = {
            "id":self.Id,
            "appId": self.appId,
            "scopeIDs": self.scopeIds,
            "description": self.description,
            "inputs":self.inputs,
            "owner":self.owner
            }
       
        print("payload:-"+str(payload)) 
        return pcc.modify_policy_by_id(conn, str(self.Id), payload)
        
    ###########################################################################
    @keyword(name="PCC.Delete Policy")
    ###########################################################################
    
    def delete_policy(self, *args, **kwargs):
        banner("PCC.Delete Policy")
        self._load_kwargs(kwargs)
        conn = BuiltIn().get_variable_value("${PCC_CONN}")
        appId = self.get_app_id_from_policies(conn,Name=self.Name) 
        Id = easy.get_policy_id(conn, Desc=self.description, AppID=appId)
        
        return pcc.delete_policy_by_id(conn, str(Id))
        
    ###########################################################################
    @keyword(name="PCC.Get Node RSOP")
    ###########################################################################
    def get_node_rsop(self,*args,**kwargs):
        self._load_kwargs(kwargs)
        banner("PCC.Get Node RSOP")
        try:
            conn = BuiltIn().get_variable_value("${PCC_CONN}")
            Id = easy.get_node_id_by_name(conn, Name=self.node_name)
        except Exception as e:
            return "Error in get_node_rsop: {}".format(e)

        response = pcc.get_node_rsop(conn,id=str(Id))
        return response
        
    ###########################################################################
    @keyword(name="PCC.Get App Details")
    ###########################################################################
    def get_app_details(self,*args,**kwargs):
        self._load_kwargs(kwargs)
        banner("PCC.Get App Details")
        conn = BuiltIn().get_variable_value("${PCC_CONN}")
        response = pcc.get_app_by_name(conn,name=self.app_name)
        return response
        
    ###########################################################################
    @keyword(name="PCC.Get Policy Deploy Status by Scopes")
    ###########################################################################
    def get_policy_deploy_status_by_scopes(self,*args,**kwargs):
        self._load_kwargs(kwargs)
        banner("PCC.Get Policy Deploy Status by Scopes")
        logger.console("Kwargs: {}".format(kwargs))
        try:
            conn = BuiltIn().get_variable_value("${PCC_CONN}")
            Id = easy.get_scope_id_by_name(conn, Name=self.scope_name, ParentID=self.parentID)
            logger.console("Id is: {}".format(Id))
        except Exception as e:
            return "Error in get_policy_deploy_status_by_scopes: {}".format(e)

        response = pcc.get_policy_deploy_status_by_scopes(conn,id=str(Id))
        return response
        
    ###########################################################################
    @keyword(name="PCC.Get Policy Deploy Status by Policies")
    ###########################################################################
    def get_policy_deploy_status_by_policies(self,*args,**kwargs):
        self._load_kwargs(kwargs)
        banner("PCC.Policy Deploy Status by Policies")
        logger.console("Kwargs: {}".format(kwargs))
        try:
            conn = BuiltIn().get_variable_value("${PCC_CONN}")
            appId = self.get_app_id_from_policies(conn,Name=self.Name) 
            Id = easy.get_policy_id(conn, Desc=self.description, AppID=appId)
            logger.console("Id is: {}".format(Id))
        except Exception as e:
            return "Error in get_policy_deploy_status_by_policies: {}".format(e)

        response = pcc.get_policy_deploy_status_by_policies(conn,id=str(Id))
        return response
        
    ###########################################################################
    @keyword(name="PCC.Apply scope to multiple nodes")
    ###########################################################################
    def apply_scope_to_multiple_nodes(self, *args, **kwargs):
        self._load_kwargs(kwargs)
        banner("PCC.Apply scope to multiple nodes")
        conn = BuiltIn().get_variable_value("${PCC_CONN}")
        print("Kwargs are: {}".format(kwargs))
        try:
            response_code_list = []
            for name in ast.literal_eval(self.node_names):
                print("Name in for loop: {}".format(name))
                node_id = Nodes().get_node_id(conn, Name=name)
                print("Node id is : {}".format(node_id))
                response = Nodes().update_node(conn, Id=node_id, Name=name, scopeId=self.scopeId)
                print("Response from update node is: {}".format(response))
                response_code_list.append(response['StatusCode'])
            print("Response code list: {}".format(response_code_list))
            result = len(response_code_list) > 0 and all(elem == 200 for elem in response_code_list)
            if result:
                return "OK"  
            else:
                return "Error: while applying scope to multiple nodes: Check response code list: {}".format(response_code_list) 
        
        except Exception as e:
            return "Error while applying scope to multiple nodes: {}".format(e)
            
            
    ###########################################################################
    @keyword(name="PCC.Check SNMP from backend")
    ###########################################################################
    def check_snmp_backend(self,**kwargs):
        banner("PCC.Check SNMP from backend")
        self._load_kwargs(kwargs)
        conn = BuiltIn().get_variable_value("${PCC_CONN}")
        cmd_snmp1="sudo systemctl status snmpd"
        cmd_snmp2="sudo netstat -anp | grep snmpd"
        cmd_snmp3="sudo ps aux | grep snmpd"
                
        success_chk = []
        failed_chk = []
        for ip in ast.literal_eval(self.targetNodeIp):
            snmp_check1=cli_run(ip,self.user,self.password,cmd_snmp1)
            print("Command_1 is: {}".format(cmd_snmp1))
            print("=========== SNMP_Check1 output ==========\n{}".format(snmp_check1))
            snmp_check2=cli_run(ip,self.user,self.password,cmd_snmp2)
            print("Command_2 is: {}".format(cmd_snmp2))
            print("=========== SNMP_Check2 output ==========\n{}".format(snmp_check2))
            snmp_check3=cli_run(ip,self.user,self.password,cmd_snmp3)
            print("Command_3 is: {}".format(cmd_snmp3))
            print("=========== SNMP_Check3 output ==========\n{}".format(snmp_check3))
            if re.search("snmpd",str(snmp_check1)) and re.search("running",str(snmp_check1)) and re.search("CONNECTED",str(snmp_check2)) and re.search("snmpd",str(snmp_check3)):
                print("SNMP Found")
                success_chk.append(ip)
                    
            else:
                failed_chk.append(ip)
        print("Success chk status is : {}".format(success_chk))
        print("Failed chk status is : {}".format(failed_chk))            
        if len(success_chk)==len(ast.literal_eval(self.targetNodeIp)):
            print("Backend verification successfuly done for : {}".format(success_chk))
            return "OK"
                                  
        if failed_chk:  
            print("SNMP service are down for {}".format(failed_chk))     
            return "Error: SNMP service are down for {}".format(failed_chk)
        else:
            return "OK"
            
    ###########################################################################
    @keyword(name="PCC.Check NTP from backend")
    ###########################################################################
    def check_ntp_backend(self,**kwargs):
        banner("PCC.Check NTP from backend")
        self._load_kwargs(kwargs)
        conn = BuiltIn().get_variable_value("${PCC_CONN}")
        cmd_ntp1="sudo systemctl status ntp"
        cmd_ntp2="sudo netstat -anp | grep ntp"
        cmd_ntp3="sudo ps aux | grep ntp"
                
        success_chk = []
        failed_chk = []
        for ip in ast.literal_eval(self.targetNodeIp):
            ntp_check1=cli_run(ip,self.user,self.password,cmd_ntp1)
            print("Command_1 is: {}".format(cmd_ntp1))
            print("=========== NTP_Check1 output ==========\n{}".format(ntp_check1))
            ntp_check2=cli_run(ip,self.user,self.password,cmd_ntp2)
            print("Command_2 is: {}".format(cmd_ntp2))
            print("=========== NTP_Check2 output ==========\n{}".format(ntp_check2))
            ntp_check3=cli_run(ip,self.user,self.password,cmd_ntp3)
            print("Command_3 is: {}".format(cmd_ntp3))
            print("=========== NTP_Check3 output ==========\n{}".format(ntp_check3))
            if re.search("ntpd",str(ntp_check1)) and re.search("running",str(ntp_check1)) and re.search("CONNECTED",str(ntp_check2)) and re.search("ntpd",str(ntp_check3)):
                print("NTP Found")
                success_chk.append(ip)
                    
            else:
                failed_chk.append(ip)
        print("Success chk status is : {}".format(success_chk))
        print("Failed chk status is : {}".format(failed_chk))            
        if len(success_chk)==len(ast.literal_eval(self.targetNodeIp)):
            print("Backend verification successfuly done for : {}".format(success_chk))
            return "OK"
                                  
        if failed_chk:  
            print("NTP service are down for {}".format(failed_chk))     
            return "Error: NTP service are down for {}".format(failed_chk)
        else:
            return "OK"
            
    ###########################################################################
    @keyword(name="PCC.Check scope assignment on node")
    ###########################################################################
    def check_scope_assignment_on_node(self,**kwargs):
        banner("PCC.Check scope assignment on node")
        self._load_kwargs(kwargs)
        logger.console("Kwargs are: {}".format(kwargs))
        conn = BuiltIn().get_variable_value("${PCC_CONN}")
        node_id = Nodes().get_node_id(conn, Name=self.node_name)
        get_node_response = Nodes().get_node(conn, Id=str(node_id))['Result']['Data']
        if str(self.scopeId) == str(get_node_response['scopeId']):
            return "OK"
        return "Error: Scope Id {} is not assigned on node {}".format(self.scopeId, self.node_name)
        
    ###########################################################################
    @keyword(name="PCC.Check policy assignment on node")
    ###########################################################################
    def check_policy_assignment_on_node(self,**kwargs):
        banner("PCC.Check policy assignment on node")
        self._load_kwargs(kwargs)
        print("Kwargs are: {}".format(kwargs))
        conn = BuiltIn().get_variable_value("${PCC_CONN}")
        node_id = Nodes().get_node_id(conn, Name=self.node_name)
        get_node_response = Nodes().get_node(conn, Id=str(node_id))['Result']['Data']
        policy_ids_from_node = get_node_response['scope']['policies']
        self.policyIDs.sort()
        policy_ids_from_node.sort()
        if self.policyIDs == policy_ids_from_node:
            return "OK"
        return "Error: Policy Ids {} are not assigned on node {}".format(self.policyIDs, self.node_name)
        
        
    ###########################################################################
    @keyword(name="PCC.Check policy assignment on scope")
    ###########################################################################
    def check_policy_assignment_on_scope(self,**kwargs):
        banner("PCC.Check policy assignment on scope")
        self._load_kwargs(kwargs)
        print("Kwargs are: {}".format(kwargs))
        conn = BuiltIn().get_variable_value("${PCC_CONN}")
        get_scope_response = self.get_scope_details(**kwargs)['Result']['Data']
        policies_from_scope = get_scope_response['policies']
        policy_ids_from_scope = []
        for policy_id in policies_from_scope:
            policy_ids_from_scope.append(policy_id['id'])
        if self.policyIDs:
            flag = 0
            user_policy_id = ast.literal_eval(self.policyIDs)
            print("policy id by user is : {}".format(user_policy_id))
            print("policy id from PCC is : {}".format(policy_ids_from_scope))
            if(set(user_policy_id).issubset(set(policy_ids_from_scope))): 
                flag = 1
            if (flag): 
                return "OK"
            else: 
                return "Error: Policy Ids {} are not assigned on node {}".format(self.policyIDs, self.scope_name)
                        
        else:
            return   "Error in else: Policy Ids {} are not assigned on node {}".format(self.policyIDs, self.scope_name)  
        
    ###########################################################################
    @keyword(name="PCC.Get Policy IDs Assigned to Scope")
    ###########################################################################
    def get_policy_ids_assigned_to_scope(self,**kwargs):
        banner("PCC.Get Policy IDs Assigned to Scope")
        self._load_kwargs(kwargs)
        print("Kwargs are: {}".format(kwargs))
        conn = BuiltIn().get_variable_value("${PCC_CONN}")
        get_scope_response = self.get_scope_details(**kwargs)['Result']['Data']
        policies_from_scope = get_scope_response['policies']
        policy_ids_from_scope = []
        for policy_id in policies_from_scope:
            policy_ids_from_scope.append(policy_id['id']) 
        if policy_ids_from_scope:
            return policy_ids_from_scope   
        else:
            return "No policies are assigned to node"   
        
        
    ###########################################################################
    @keyword(name="PCC.Check roles assignment on node")
    ###########################################################################
    def check_roles_assignment_on_node(self,**kwargs):
        banner("PCC.Check roles assignment on node")
        self._load_kwargs(kwargs)
        print("Kwargs are: {}".format(kwargs))
        conn = BuiltIn().get_variable_value("${PCC_CONN}")
        node_id = Nodes().get_node_id(conn, Name=self.node_name)
        get_node_response = Nodes().get_node(conn, Id=str(node_id))['Result']['Data']
        
        roles_from_node = get_node_response['roles']
        if self.roles_id:
            flag = 0
            user_role_id = ast.literal_eval(self.roles_id)
            print("role id by user is : {}".format(user_role_id))
            print("role id from PCC is : {}".format(roles_from_node))
            if(set(user_role_id).issubset(set(roles_from_node))): 
                flag = 1
            if (flag): 
                return "OK"
            else: 
                return "Error: Role Ids {} are not assigned on node {}".format(self.roles_id, self.scope_name)
                        
        else:
            return   "Error in else: Role Ids {} are not assigned on node {}".format(self.roles_id, self.scope_name)
         
    ###########################################################################
    @keyword(name="PCC.Get roles assigned to node")
    ###########################################################################
    def get_roles_assigned_to_node(self,**kwargs):
        banner("PCC.Get roles assigned to node")
        self._load_kwargs(kwargs)
        print("Kwargs are: {}".format(kwargs))
        conn = BuiltIn().get_variable_value("${PCC_CONN}")
        node_id = Nodes().get_node_id(conn, Name=self.node_name)
        get_node_response = Nodes().get_node(conn, Id=str(node_id))['Result']['Data']
        
        roles_from_node = get_node_response['roles']
        if roles_from_node:
            return roles_from_node
        else:
            return "No roles assigned to node"
            
        
    
    
    