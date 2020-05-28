package main

import(
	"fmt"
	"flag"
	"os"
	"encoding/json"
	"context"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/tools/clientcmd"
	appsv1 "k8s.io/api/apps/v1"
	apiv1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"github.com/ghodss/yaml"
)

type microService struct{
	name string
	deployment string
	deploymentPath string
	pod string
	podPath string
	service string
	servicePath string
	pvc string
	pvcPath string
	pv string
	pvPath string
	dbdeployment string
	dbdeploymentPath string
	dbservice string
	dbservicePath string
	dbpod string
	dbpodPath string
}


//Creation of microservice struct literals
var (
	orderService  = microService{	name: "order",
									deployment: "order-deployment",
									deploymentPath: "../deployments/order/order_deployment.yaml",
									service : "order-service",
									servicePath : "../deployments/order/order_service.yaml",
									dbdeployment : "mysql-deployment",
									dbdeploymentPath : "../deployments/order/mysql_deployment.yaml",
									dbservice : "mysql-service",
									dbservicePath : "../deployments/order/mysql_service.yaml",
									pvc : "mysql-pvc",
									pvcPath : "../deployments/order/mysql_pvc.yaml",
									pv : "mysql-pv",
									pvPath : "../deployments/order/mysql_pv.yaml",
							}

	userService  = microService{
									name: "user",
									deployment: "user-deployment",
									deploymentPath : "../deployments/user/user_deployment.yaml",
									service : "user-service",
									servicePath : "../deployments/user/user_service.yaml",
									dbdeployment : "postgres-deployment",
									dbdeploymentPath : "../deployments/user/postgres-deployment.yaml",
									dbservice : "postgres-user",
									dbservicePath : "../deployments/user/postgres_service.yaml",
									pvc : "postgres-pvc",
									pvcPath : "../deployments/user/user_pvc.yaml",
									pv : "postgres-pv",
									pvPath : "../deployments/user/user_pv.yaml",
							}

    logisticsService  = microService{
									name: "logistics",
									deployment: "logistics-deployment",
									deploymentPath : "../deployments/logistics/logistics_deployment.yaml",
									service : "logistics-service",
									servicePath : "../deployments/logistics/logistics_service.yaml",
									dbdeployment : "postgres-logistics-deployment",
									dbdeploymentPath : "../deployments/logistics/postgres_logistics_deployment.yaml",
									dbservice : "postgres-logistic",
									dbservicePath : "../deployments/logistics/postgres_logistics_service.yaml",
									pvc : "postgres-logistics-pvc",
									pvcPath : "../deployments/logistics/logistics_pvc.yaml",
									pv : "postgres-logistics-pv",
									pvPath : "../deployments/logistics/logistics_pv.yaml",
							}

	gatewayService  = microService{
									name: "gateway",
									deployment: "gateway-deployment",
									deploymentPath : "../deployments/gateway/gateway_deployment.yaml",
									service : "gateway-service",
									servicePath : "../deployments/gateway/gateway_service.yaml",
									dbpod : "redis-pod",
									dbpodPath : "../deployments/gateway/redis_pod.yaml",
									dbservice : "redis-service",
									dbservicePath : "../deployments/gateway/redis_service.yaml",
							}
)


//Function to read in a .yaml file and return it as a map
func readConfigFile(filepath string)map[string]interface{}{
	file , err := os.Open(filepath)
	if err != nil{
		panic(err)
	}
	defer file.Close()

	fileInfo ,err := file.Stat()
	if err != nil{
		panic(err)
	}

	buffer := make([]byte , fileInfo.Size())
	_ , err = file.Read(buffer)
	if err != nil{
		panic(err)
	}

	filejson , err := yaml.YAMLToJSON(buffer)
	if err != nil{
		panic(err)
	}

	m := make(map[string]interface{})
	json.Unmarshal(filejson , &m)
	// fmt.Printf("%#v" , m["kind"])
	
	return m
}

/*
Creates a service based on the configuration file present at some location
Parameters:
clientset : *kubernetes.Clientset : API client object
path      : string                : Path of config file to be created
*/
func createSerivce(clientset *kubernetes.Clientset , path string){
	mapjson := readConfigFile(path)
	var service apiv1.Service
	stringjson , _ := json.Marshal(mapjson)
	json.Unmarshal(stringjson , &service)

	serviceClient := clientset.CoreV1().Services(apiv1.NamespaceDefault)
	fmt.Printf("Created service client !\n")
	res , err := serviceClient.Create(context.TODO() , &service , metav1.CreateOptions{})
	if err != nil{
		panic(err)
	}
	fmt.Printf("Created Service %q.\n", res.GetObjectMeta().GetName())
}

/*
Creates a deployment based on the configuration file present at some location
Parameters:
clientset : *kubernetes.Clientset : API client object
path      : string                : Path of config file to be created
*/
func createDeployment(clientset *kubernetes.Clientset , path string){
	mapjson := readConfigFile(path)
	var dep appsv1.Deployment
	stringjson , _ := json.Marshal(mapjson)
	json.Unmarshal(stringjson , &dep)

	deploymentClient := clientset.AppsV1().Deployments(apiv1.NamespaceDefault)
	fmt.Printf("Created dep client !\n")
	res , err := deploymentClient.Create(context.TODO() , &dep , metav1.CreateOptions{})
	if err != nil{
		panic(err)
	}
	fmt.Printf("Created deployment %q.\n", res.GetObjectMeta().GetName())
}

/*
Creates a pod based on the configuration file present at some location
Parameters:
clientset : *kubernetes.Clientset : API client object
path      : string                : Path of config file to be created
*/
func createPod(clientset *kubernetes.Clientset , path string){
	mapjson := readConfigFile(path)
	var pod apiv1.Pod
	stringjson , _ := json.Marshal(mapjson)
	json.Unmarshal(stringjson , &pod)

	podClient := clientset.CoreV1().Pods(apiv1.NamespaceDefault)
	fmt.Printf("Created pod client !\n")
	res , err := podClient.Create(context.TODO() , &pod , metav1.CreateOptions{})
	if err != nil{
		panic(err)
	}
	fmt.Printf("Created pod %q.\n", res.GetObjectMeta().GetName())
}

func (mService *microService)CreateResources(clientset *kubernetes.Clientset){

	//Check whether database service object is present. If not creates one. 
	if mService.dbservice != "" && !serviceExists(clientset , mService.dbservice){
		createSerivce(clientset , mService.dbservicePath)
	}
	//Check whether database deployment object is present. If not creates one.
	if mService.dbdeployment != "" && !deploymentExists(clientset , mService.dbdeployment){
		createDeployment(clientset , mService.dbdeploymentPath)
	}
	//Check whether database pod object is present. If not creates one.
	if mService.dbpod != "" && !podExists(clientset , mService.dbpod){
		createPod(clientset , mService.dbpodPath)
	}	
	//Check whether service object is present. If not creates one.
	if mService.service != "" && !serviceExists(clientset , mService.service){
		createSerivce(clientset , mService.servicePath)
	}
	//Check whether deployment object is present. If not creates one.
	if mService.deployment != "" && !deploymentExists(clientset , mService.deployment){
		createDeployment(clientset , mService.deploymentPath)
	}


}


//Function to check whether all components of a micro service exist ot not
func(mService *microService)microServiceExists(clientset *kubernetes.Clientset)bool{
	if mService.pv != "" && !pvExists(clientset , mService.pv){
		fmt.Printf("%s not present !")
		return false
	}
	if mService.pvc != "" && !pvcExists(clientset , mService.pvc){
		return false
	}
	if mService.service !="" && !serviceExists(clientset , mService.service){
		return false
	}
	if mService.deployment != "" && !deploymentExists(clientset , mService.deployment){
		return false
	}
	if mService.pod != "" && !podExists(clientset , mService.pod){
		return false
	}
	if mService.dbdeployment != "" && !deploymentExists(clientset , mService.dbdeployment){
		return false
	}
	if mService.dbservice != "" && !serviceExists(clientset , mService.dbservice){
		return false
	}
	if mService.dbpod != "" && !podExists(clientset , mService.dbpod){
		return false
	}

	return true
}

//Function to check whether a Persistent volume exists or not
func pvExists(clientset *kubernetes.Clientset , pvName string) bool{
	pvClient := clientset.CoreV1().PersistentVolumes()
	list , err := pvClient.List(context.TODO() , metav1.ListOptions{})
	if err != nil{
		panic(err)
	}

	for _ , pv := range list.Items{
		if pv.ObjectMeta.Name == pvName{
			fmt.Printf("%s pv exists in default namespace !\n" , pvName)
			return true
		}
	}
	return false
}
	
//Function to check whether a Persistent volume claim exists or not
func pvcExists(clientset *kubernetes.Clientset , pvcName string) bool{
	pvcClient := clientset.CoreV1().PersistentVolumeClaims(apiv1.NamespaceDefault)
	list , err := pvcClient.List(context.TODO() , metav1.ListOptions{})
	if err != nil{
		panic(err)
	}

	for _ , pvc := range list.Items{
		if pvc.ObjectMeta.Name == pvcName{
			fmt.Printf("%s pvc exists in default namespace !\n" , pvcName)
			return true
		}
	}
	return false
}

//Function to check whether a pod exists or not
func podExists(clientset *kubernetes.Clientset , podName string)bool{
	podClient := clientset.CoreV1().Pods(apiv1.NamespaceDefault)
	list , err := podClient.List(context.TODO() , metav1.ListOptions{})
	if err != nil{
		panic(err)
	}

	for _ , pod := range list.Items{
		if pod.ObjectMeta.Name == podName{
			fmt.Printf("%s pod exists in default namespace !\n" , podName)
			return true
		}
	}
	return false
}

//Function to check whether a service exists or not
func serviceExists(clientset *kubernetes.Clientset , serviceName string)bool{
	serviceClient := clientset.CoreV1().Services(apiv1.NamespaceDefault)
	list , err := serviceClient.List(context.TODO() , metav1.ListOptions{})
	if err != nil{
		panic(err)
	}

	for _ , svc := range list.Items{
		if svc.ObjectMeta.Name == serviceName{
			fmt.Printf("%s service exists in default namespace !\n" , serviceName)
			return true
		}
	}
	return false
}

//TODO add checks for status of pods
//Function to check whether a deployment exists or not
func deploymentExists(clientset * kubernetes.Clientset , deploymentName string) bool{
	deploymentClient := clientset.AppsV1().Deployments(apiv1.NamespaceDefault)
	list , err := deploymentClient.List(context.TODO() , metav1.ListOptions{})
	if err != nil{
		panic(err)
	}

	for _ , dep := range list.Items{
		if dep.ObjectMeta.Name == deploymentName{
			fmt.Printf("%s exists in default namespace !\n" , deploymentName)
			return true
		}
	}
	return false
}

func main(){
	var kubeconfig *string

	kubeconfig = flag.String("kubeconfig","","absolute path to kubeconfig file")
	flag.Parse()

	config , err := clientcmd.BuildConfigFromFlags("",*kubeconfig)
	if err!=nil{
		panic(err)
	}
	
	clientset , err := kubernetes.NewForConfig(config)
	if err != nil{
		panic(err)
	}

	orderService.CreateResources(clientset)
	userService.CreateResources(clientset)
	logisticsService.CreateResources(clientset)
	gatewayService.CreateResources(clientset)

	// readConfigFile("../deployments/order/order_deployment.yaml")


}