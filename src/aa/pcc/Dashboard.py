import time
import json
import ast
import math

from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.BuiltIn import RobotNotRunningError

from platina_sdk import pcc_api as pcc
from aa.common import PccUtility as easy

from aa.common.Utils import banner, trace, pretty_print, cmp_json
from aa.common.Result import get_response_data
from aa.common.AaBase import AaBase
from aa.common.Cli import cli_run

PCCSERVER_TIMEOUT = 60 * 10


class Dashboard(AaBase):
    def __init__(self):
        self.k8s = None
        self.nwtcluster = None
        self.nodes = None
        self.objects = None
        self.cephcluster_name = None
        self.nodeip = None
        self.user = "pcc"
        self.password = "cals0ft"
        super().__init__()

    ###########################################################################
    @keyword(name="PCC.Dashboard Verify object graph")
    ###########################################################################
    def verify_object_graph(self, *arg, **kwargs):
        banner("PCC.Dashboard verify object graph")
        self._load_kwargs(kwargs)
        print("Kwargs:" + str(kwargs))
        try:
            conn = BuiltIn().get_variable_value("${PCC_CONN}")
        except Exception as e:
            raise e

        response = pcc.get_object_graph(conn)
        print("Response:" + str(response))
        failed_objects = []
        for object in eval(str(self.objects)):
            if object in get_response_data(response):
                continue
            else:
                failed_objects.append(object)
        if failed_objects:
            print("Could not verified following objects " + str(failed_objects))
            return "Error"
        else:
            print("All of {} are verified".format(self.objects))
            return "OK"

    ###########################################################################
    @keyword(name="PCC.Dashboard verify object count")
    ###########################################################################
    def verify_object_count(self, *arg, **kwargs):
        banner("PCC.Dashboard verify object count")
        self._load_kwargs(kwargs)
        print("Kwargs:" + str(kwargs))
        try:
            conn = BuiltIn().get_variable_value("${PCC_CONN}")
        except Exception as e:
            raise e
        response = pcc.get_object_graph(conn)
        print("Response:" + str(response))
        failed_objects1 = []
        for object in eval(str(self.objects)):
            if object == "Node":
                response1 = pcc.get_nodes(conn)
                data1 = get_response_data(response1)
                count = len(data1)
                data2 = get_response_data(response)
                count1 = data2["Node"]['countTotal']
                if count == count1:
                    print("Correct Node count : {}".format(count))
                    continue
                else:
                    failed_objects1.append(object)

            elif object == "CephCluster":
                response1 = pcc.get_ceph_clusters(conn)
                data1 = get_response_data(response1)
                count = len(data1)
                data2 = get_response_data(response)
                count1 = data2["CephCluster"]['countTotal']
                if count == count1:
                    print("Correct ceph count : {}".format(count))
                else:
                    failed_objects1.append(object)

            elif object == "NetworkCluster":
                response1 = pcc.get_network_clusters(conn)
                data1 = get_response_data(response1)
                count = len(data1)
                data2 = get_response_data(response)
                count1 = data2["NetworkCluster"]['countTotal']
                if count == count1:
                    print("Correct network count : {}".format(count))
                else:
                    failed_objects1.append(object)

            elif object == "K8sCluster":
                response1 = pcc.get_kubernetes(conn)
                data1 = get_response_data(response1)
                count = len(data1)
                data2 = get_response_data(response)
                count1 = data2["K8sCluster"]['countTotal']
                if count == count1:
                    print("Correct k8s count : {}".format(count))
                else:
                    failed_objects1.append(object)

        if failed_objects1:
            print("Could not verified following objects " + str(failed_objects1))
            return "Count Comparison Failed"
        else:
            print("All of {} are verified".format(self.objects))
            return "OK"

    ###########################################################################
    @keyword(name="PCC.Dashboard Verify object health")
    ###########################################################################
    def verify_object_health(self, *arg, **kwargs):
        banner("PCC.Dashboard verify object health")
        self._load_kwargs(kwargs)
        print("Kwargs:" + str(kwargs))
        try:
            conn = BuiltIn().get_variable_value("${PCC_CONN}")
        except Exception as e:
            raise e
        response = pcc.get_object_graph(conn)
        print("Response:" + str(response))
        failed_objects1 = []
        okcount = 0
        warningcount = 0
        errorcount = 0

        for object in eval(str(self.objects)):
            if object == "K8sCluster":
                response1 = pcc.get_kubernetes(conn)
                data1 = get_response_data(response1)
                count = len(data1)
                for x in range(count):
                    data = data1[x]
                    if data["healthStatus"] == "good":
                        okcount += 1
                    elif data["healthStatus"] == "warning":
                        warningcount += 1
                    elif data["healthStatus"] == "notok":
                        errorcount += 1
                    else:
                        print("k8s health count is missing on k8s cluster page")
                data2 = get_response_data(response)
                count1 = data2["K8sCluster"]['countOK']
                count2 = data2["K8sCluster"]["countWarning"]
                count3 = data2["K8sCluster"]["countNotOK"]
                if count1 == okcount:
                    print("Correct k8s OK count : {}".format(okcount))
                elif count2 == warningcount:
                    print("Correct k8s Warning count : {}".format(warningcount))
                elif count3 == errorcount:
                    print("Correct k8s Error count : {}".format(errorcount))
                else:
                    failed_objects1.append(object)

            if object == "Node":
                response1 = pcc.get_nodes(conn)
                data1 = get_response_data(response1)
                count = len(data1)
                for x in range(count):
                    data = data1[x]
                    if data["status"] == "OK":
                        okcount += 1
                    elif data["status"] == "WARNING":
                        warningcount += 1
                    elif data["status"] == "NOTOK":
                        errorcount += 1
                    else:
                        print("Nodes health count is missing on Node summary page")
                data2 = get_response_data(response)
                count1 = data2["Node"]['countOK']
                count2 = data2["Node"]["countWarning"]
                count3 = data2["Node"]["countNotOK"]
                if count1 == okcount:
                    print("Correct node OK count : {}".format(okcount))
                elif count2 == warningcount:
                    print("Correct node Warning count : {}".format(warningcount))
                elif count3 == errorcount:
                    print("Correct node Error count : {}".format(errorcount))
                else:
                    failed_objects1.append(object)

            if object == "CephCluster":
                response1 = pcc.get_ceph_clusters(conn)
                data1 = get_response_data(response1)
                count = len(data1)
                for x in range(count):
                    data = data1[x]
                    if data["status"] == "OK":
                        okcount += 1
                    elif data["status"] == "WARNING":
                        warningcount += 1
                    elif data["status"] == "NOTOK":
                        errorcount += 1
                    else:
                        print("Nodes health count is missing on Node summary page")
                data2 = get_response_data(response)
                count1 = data2["Node"]['countOK']
                count2 = data2["Node"]["countWarning"]
                count3 = data2["Node"]["countNotOK"]
                if count1 == okcount:
                    print("Correct node OK count : {}".format(okcount))
                elif count2 == warningcount:
                    print("Correct node Warning count : {}".format(warningcount))
                elif count3 == errorcount:
                    print("Correct node Error count : {}".format(errorcount))
                else:
                    failed_objects1.append(object)

            if object == "NetworkCluster":
                response1 = pcc.get_network_clusters(conn)
                data1 = get_response_data(response1)
                count = len(data1)
                for x in range(count):
                    data = data1[x]
                    if data["health"] == "OK":
                        okcount += 1
                    elif data["health"] == "WARNING":
                        warningcount += 1
                    elif data["health"] == "NOTOK":
                        errorcount += 1
                    else:
                        print("Network health count is missing on Network cluster page")
                data2 = get_response_data(response)
                count1 = data2["Node"]['countOK']
                count2 = data2["Node"]["countWarning"]
                count3 = data2["Node"]["countNotOK"]
                if count1 == okcount:
                    print("Correct node OK count : {}".format(okcount))
                elif count2 == warningcount:
                    print("Correct node Warning count : {}".format(warningcount))
                elif count3 == errorcount:
                    print("Correct node Error count : {}".format(errorcount))
                else:
                    failed_objects1.append(object)
        if failed_objects1:
            print("Could not verified following objects " + str(failed_objects1))
            return "Health Comparison Failed"
        else:
            print("All of {} are verified".format(self.objects))
            return "OK"

    ###########################################################################
    @keyword(name="PCC.Dashboard Verify object metrics")
    ###########################################################################
    def verify_object_metrics(self, *arg, **kwargs):
        banner("PCC.Dashboard Verify object metrics")
        self._load_kwargs(kwargs)
        print("Kwargs:" + str(kwargs))
        try:
            conn = BuiltIn().get_variable_value("${PCC_CONN}")
        except Exception as e:
            raise e
        response = pcc.get_object_metrics(conn)
        print("Response:" + str(response))
        failed_objects = []
        for object in eval(str(self.objects)):
            if object == "Node":
                for data in get_response_data(response):
                    if data["pccObjectType"] == "Node":
                        for item in data["metricsList"]:
                            if item["metricName"] == "cpuLoad":
                                print("Node metric cpu load is correct")
                            elif item["metricName"] == "usedMemory":
                                print("Node metric used memory is correct")
                            else:
                                print("Metrics is not showing for {} node".format(data["pccObjectName"]))
                                failed_objects.append(data["pccObjectType"])

            elif object == "CephCluster":
                for data in get_response_data(response):
                    if data["pccObjectType"] == "CephCluster":
                        for item in data["metricsList"]:
                            if item["metricName"] == "capacityUsed":
                                print("Ceph cluster capacity metric is showing on the Summary page")
                            else:
                                print("Metrics is not showing for {} node".format(data["pccObjectName"]))
                                failed_objects.append(data["pccObjectType"])
            elif object == "K8sCluster":
                for data in get_response_data(response):
                    if data["pccObjectType"] == object:
                        for item in data["metricsList"]:
                            if item["metricName"] == "cpuLoad":
                                print("Node metric cpu load is correct")
                            elif item["metricName"] == "usedMemory":
                                print("Node metric used memory is correct")
                            else:
                                print("Metrics is not showing for {} node".format(data["pccObjectName"]))
                                failed_objects.append(data["pccObjectType"])

            else:
                print("{} object not found".format(object))

            if failed_objects:
                print("Could not verified following objects " + str(failed_objects))
                return "Metric Comparison Failed"
            else:
                print("All of {} are verified".format(self.objects))
                return "OK"

    ###########################################################################
    @keyword(name="PCC.Dashboard Verify object location")
    ###########################################################################
    def verify_object_location(self, *arg, **kwargs):
        banner("PCC.Dashboard Verify object location")
        self._load_kwargs(kwargs)
        print("Kwargs:" + str(kwargs))
        try:
            conn = BuiltIn().get_variable_value("${PCC_CONN}")
        except Exception as e:
            raise e
        dashboard_response = pcc.get_object_metrics(conn)
        nodesummary_response = pcc.get_nodes(conn)
        failed_objects = []
        dashboard_dict = {}
        node_summary_dict = {}

        ### Parsing Dashboard data
        for object in eval(str(self.objects)):
            if object == "Node":
                for data in get_response_data(dashboard_response):
                    if data["pccObjectType"] == object:
                        node_name = data["pccObjectName"]
                        for item in data["scopes"][0]:
                            location_id = item["id"]
                            break
                        dashboard_dict[node_name] = location_id

        ### Parsing Nodesummary data
        for data in get_response_data(nodesummary_response):
            node_name_from_nodesummary = data['Name']
            scope_id = data['scope']['id']
            node_summary_dict[node_name_from_nodesummary] = scope_id

        if dashboard_dict == node_summary_dict:
            return "OK"
        else:
            return "Location Validation failed"

    ###########################################################################
    @keyword(name="PCC.Dashboard Verify Object Health/Kernel/OS Information")
    ###########################################################################
    def verify_object_information(self, *arg, **kwargs):
        banner("PCC.Dashboard Verify object location")
        self._load_kwargs(kwargs)
        print("Kwargs:" + str(kwargs))
        try:
            conn = BuiltIn().get_variable_value("${PCC_CONN}")
        except Exception as e:
            raise e
        dashboard_response = pcc.get_object_metrics(conn)
        k8s_response = pcc.get_kubernetes(conn)
        ceph_clusters_response = pcc.get_ceph_clusters(conn)
        network_cluster_response = pcc.get_network_clusters(conn)
        node_summary_response = pcc.get_nodes(conn)

        failed_objects = []
        ceph_cluster_dashboard_dict = {}
        ceph_cluster_dict = {}
        k8s_dashboard = {}
        network_dashboard = {}
        network_cluster = {}
        node_dashboard = {}
        node_summary = {}
        k8s_cluster = {}

        for object in eval(str(self.objects)):
            for data in get_response_data(dashboard_response):
                if object == "K8sCluster":
                    if data["pccObjectType"] == object:
                        k8s_dashboard["Name"] = data["pccObjectName"]
                        k8s_dashboard["Health"] = data["health"]["description"].lower()

                        for data1 in get_response_data(k8s_response):
                            if data1["name"] == k8s_dashboard["Name"]:
                                k8s_cluster["Name"] = data1["name"]
                                k8s_cluster["Health"] = data1["healthStatus"]
    
                        if k8s_cluster == k8s_dashboard:
                            print("Correct K8s information")
                        else:
                            failed_objects.append(k8s_dashboard["Name"])

                if object == "CephCluster":
                    if data["pccObjectType"] == object:
                        ceph_cluster_dashboard_dict["Name"] = data["pccObjectName"]
                        ceph_dashboard_description = data["health"]["description"]
                        ceph_cluster_dashboard_dict["Health"] = ''.join(
                            e for e in ceph_dashboard_description if e.isalnum())

                        for item in data["pccObjectDetails"]:
                            if item["topic"] == "Total Capacity":
                                capacity_value = str(math.ceil(eval(item["message"].split(" ")[0]))) + " " + \
                                                 item["message"].split(" ")[1]
                                ceph_cluster_dashboard_dict["Total Capacity"] = capacity_value
                            elif item["topic"] == "Version":
                                ceph_cluster_dashboard_dict["Version"] = item["message"]

                        for ceph in get_response_data(ceph_clusters_response):
                            if ceph["name"] == ceph_cluster_dashboard_dict["Name"]:
                                ceph_cluster_dict["Name"] = ceph["name"]
                                ceph_id = easy.get_ceph_cluster_id_by_name(conn, ceph["name"])
                                ceph_response = pcc.get_ceph_cluster_health_by_id(conn, str(ceph_id))
    
                                ceph_health_response = get_response_data(ceph_response)
    
                                ceph_cluster_description = ceph_health_response["summary"]
                                ceph_cluster_dict["Health"] = ''.join(e for e in ceph_cluster_description if e.isalnum())
                                cmd1 = 'sudo /opt/platina/pcc/bin/systemCollector lastsample ceph-metrics|grep version|tr -s " "|cut -d ":" -f2|xargs'
                                cmd2 = 'sudo ceph -s | grep usage | cut -d "/" -f2 | cut -d "a" -f1'
                                cmd_execution = cli_run(self.nodeip, self.user, self.password, cmd1)
    
                                cmd_execution_2 = cli_run(self.nodeip, self.user, self.password, cmd2)
                                serialise_output_1 = self._serialize_response(time.time(), cmd_execution)['Result'][
                                    'stdout']
                                ceph_cluster_dict["Version"] = serialise_output_1.strip()
                                serialise_output_2 = self._serialize_response(time.time(), cmd_execution_2)['Result'][
                                    'stdout']
                                ceph_cluster_dict["Total Capacity"] = serialise_output_2.strip()
    
                        if ceph_cluster_dashboard_dict == ceph_cluster_dict:
                            print("Ceph cluster related information is correct")
                        else:
                            failed_objects.append(ceph_cluster_dashboard_dict["Name"])
                elif object == "NetworkCluster":
                    if data["pccObjectType"] == object:
                        network_dashboard["Name"] = data["pccObjectName"]
                        network_dashboard["Health"] = data["health"]["health"]
                        print("network Dashboard : {}".format(network_dashboard))
                        for network in get_response_data(network_cluster_response):
                            if network["name"] == network_dashboard["Name"]:
                                network_cluster["Name"] = network["name"]
                                network_cluster["Health"] = network["health"]
    
                        print("Network Cluster : {}".format(network_cluster))
                        if network_dashboard == network_cluster:
                            print("Network cluster related information is correct")
                        else:
                            failed_objects.append(network_dashboard["Name"])

                elif object == "Node":
                    if data["pccObjectType"] == object:
                        node_dashboard["Name"] = data["pccObjectName"]
                        for item in data["pccObjectDetails"]:
                            if item["topic"] == "Kernel":
                                node_dashboard["Kernel"] = item["message"].lower()
                            elif item["topic"] == "OS":
                                node_dashboard["OS"] = item["message"].lower()
                        trace("Node Dashboard: {}".format(node_dashboard))
                        for data in get_response_data(node_summary_response):
                            if data["Name"] == node_dashboard["Name"]:
                                if "Id" in data:
                                    id = data["Id"]
                                elif "nodeId" in data:
                                    id = data["nodeId"]
    
                                get_node_response = get_response_data(pcc.get_node_by_id(conn, str(id)))
                                node_summary["Name"] = data["Name"]
    
                                node_summary["Kernel"] = str(get_node_response["systemData"]["kernel"].lower()).strip()
    
                                node_summary["OS"] = str(
                                    get_node_response["systemData"]["osName"].lower()).strip() + " " + str(
                                    get_node_response["systemData"]["baseIso"].lower()).strip()
    
                            trace("Node summary: {}".format(node_summary))

                        if node_summary == node_dashboard:
                            print("Node related information is correct")
                        else:
                            failed_objects.append(node_dashboard["Name"])

        if failed_objects:
            trace("Following objects are failed : {}".format(failed_objects))
            return "Comparison failed"
        else:
            return "OK"