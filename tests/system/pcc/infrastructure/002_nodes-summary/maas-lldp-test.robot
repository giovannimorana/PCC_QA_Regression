*** Settings ***
Resource    pcc_resources.robot

*** Variables ***
${pcc_setup}                 pcc_212

*** Test Cases ***
###################################################################################################################################
Login
###################################################################################################################################

                                    Load Clusterhead 1 Test Data        ${pcc_setup}
                                    Load Clusterhead 2 Test Data        ${pcc_setup}
                                    Load Server 2 Test Data        ${pcc_setup}
                                    Load Server 1 Test Data        ${pcc_setup}
                                    
        ${status}                   Login To PCC        testdata_key=${pcc_setup}
                                    Should Be Equal     ${status}  OK


###################################################################################################################################
Adding Mass To Invaders
###################################################################################################################################
    [Documentation]                 *Adding Mass To Invaders*
                               ...  Keywords:
                               ...  PCC.Add and Verify Roles On Nodes
                               ...  PCC.Wait Until Roles Ready On Nodes

        ${response}                 PCC.Add and Verify Roles On Nodes
                               ...  nodes=["${CLUSTERHEAD_1_NAME}"]
                               ...  roles=["Baremetal Management Node"]

                                    Should Be Equal As Strings      ${response}  OK

        ${status_code}              PCC.Wait Until Roles Ready On Nodes
                               ...  node_name=${CLUSTERHEAD_1_NAME}                                     
                                    Should Be Equal As Strings      ${status_code}  OK     

        ${response}                 PCC.Mass Verify BE
                               ...  nodes_ip=["${CLUSTERHEAD_1_HOST_IP}"]
                               ...  user=${PCC_LINUX_USER}
                               ...  password=${PCC_LINUX_PASSWORD}
                                    Should Be Equal As Strings      ${response}  OK                                      
                                    
###################################################################################################################################
Adding LLDP To Invaders
###################################################################################################################################
    [Documentation]                 *Adding LLDP To Invaders*
                               ...  Keywords:
                               ...  PCC.Add and Verify Roles On Nodes
                               ...  PCC.Wait Until Roles Ready On Nodes

        ${response}                 PCC.Add and Verify Roles On Nodes
                               ...  nodes=["${CLUSTERHEAD_1_NAME}"]
                               ...  roles=["Default"]
                                    Should Be Equal As Strings      ${response}  OK

        ${status_code}              PCC.Wait Until Roles Ready On Nodes
                               ...  node_name=${CLUSTERHEAD_1_NAME}                                     
                                    Should Be Equal As Strings      ${status_code}  OK     

        ${response}                 PCC.Lldp Verify BE
                               ...  nodes_ip=["${CLUSTERHEAD_1_HOST_IP}"]
                               ...  user=${PCC_LINUX_USER}
                               ...  password=${PCC_LINUX_PASSWORD}
                                    Should Be Equal As Strings      ${response}  OK
                                    
###################################################################################################################################
Adding Mass+LLDP To Invaders
###################################################################################################################################
    [Documentation]                 *Adding Mass+LLDP To Invaders*
                               ...  Keywords:
                               ...  PCC.Add and Verify Roles On Nodes
                               ...  PCC.Wait Until Roles Ready On Nodes

        ${response}                 PCC.Add and Verify Roles On Nodes
                               ...  nodes=["${CLUSTERHEAD_1_NAME}"]
                               ...  roles=["Baremetal Management Node","Default"]

                                    Should Be Equal As Strings      ${response}  OK

        ${status_code}              PCC.Wait Until Roles Ready On Nodes
                               ...  node_name=${CLUSTERHEAD_1_NAME}                                     
                                    Should Be Equal As Strings      ${status_code}  OK     

        ${response}                 PCC.Mass Verify BE
                               ...  nodes_ip=["${CLUSTERHEAD_1_HOST_IP}"]
                               ...  user=${PCC_LINUX_USER}
                               ...  password=${PCC_LINUX_PASSWORD}
                                    Should Be Equal As Strings      ${response}  OK    

        ${response}                 PCC.Lldp Verify BE
                               ...  nodes_ip=["${CLUSTERHEAD_1_HOST_IP}"]
                               ...  user=${PCC_LINUX_USER}
                               ...  password=${PCC_LINUX_PASSWORD}
                                    Should Be Equal As Strings      ${response}  OK                                    
###################################################################################################################################
Adding LLDP To Server
###################################################################################################################################
    [Documentation]                 *Adding LLDP To Server*
                               ...  Keywords:
                               ...  PCC.Add and Verify Roles On Nodes
                               ...  PCC.Wait Until Roles Ready On Nodes

        ${response}                 PCC.Add and Verify Roles On Nodes
                               ...  nodes=["${SERVER_2_NAME}"]
                               ...  roles=["Default"]
                                    Should Be Equal As Strings      ${response}  OK

        ${status_code}              PCC.Wait Until Roles Ready On Nodes
                               ...  node_name=${SERVER_2_NAME}
                                    Should Be Equal As Strings      ${status_code}  OK     

        ${response}                 PCC.Lldp Verify BE
                               ...  nodes_ip=["${SERVER_2_NAME}"]
                               ...  user=${PCC_LINUX_USER}
                               ...  password=${PCC_LINUX_PASSWORD}
                                    Should Be Equal As Strings      ${response}  OK                                      
###################################################################################################################################
#Adding Maas To Server (Negative)
####################################################################################################################################
#    [Documentation]                 *Adding Maas To Server*
#                               ...  Keywords:
#                               ...  PCC.Add and Verify Roles On Nodes
#                               ...  PCC.Wait Until Roles Ready On Nodes
#
#        ${response}                 PCC.Add and Verify Roles On Nodes
#                               ...  nodes=["${SERVER_2_NAME}"]
#                               ...  roles=["Baremetal Management Node"]
#                                    Should Be Equal As Strings      ${response}  OK
#
#        ${status_code}              PCC.Wait Until Roles Ready On Nodes
#                               ...  node_name=${SERVER_2_NAME}                                    
#                                    Should Not Be Equal As Strings      ${status_code}  OK
#
###################################################################################################################################
Deleting Mass From Nodes
###################################################################################################################################
    [Documentation]                 *Deleting Mass+LLDP From Nodes*
                               ...  Keywords:
                               ...  PCC.Delete and Verify Roles On Nodes
                               ...  PCC.Wait Until Roles Ready On Nodes
                               
        ${response}                 PCC.Delete and Verify Roles On Nodes
                               ...  nodes=["${CLUSTERHEAD_1_NAME}"]
                               ...  roles=["Baremetal Management Node"]
                                    Should Be Equal As Strings      ${response}  OK

        ${status_code}              PCC.Wait Until Roles Ready On Nodes
                               ...  node_name=${CLUSTERHEAD_1_NAME}
                                    Should Be Equal As Strings      ${status_code}  OK

        ${response}                 PCC.Mass Verify BE
                               ...  nodes_ip=["${CLUSTERHEAD_1_HOST_IP}"]
                               ...  user=${PCC_LINUX_USER}
                               ...  password=${PCC_LINUX_PASSWORD}
                                    Should Not Be Equal As Strings      ${response}  OK
                                    
