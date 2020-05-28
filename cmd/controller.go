package main

import(
	"fmt"
	"context"
	"encoding/json"
	"os"
	"flag"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/tools/clientcmd"
	appsv1 "k8s.io/api/apps/v1"
	apiv1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/watch"
	"github.com/ghodss/yaml"
)

//Generalised struct for a micro service
//Contains names of "Api objects" and their relative path in the deployments folder
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
Watches for changes in status of service objects.
Creates a service object if gets a "Deleted" notification
*/
func watchService(clientset *kubernetes.Clientset){
	serviceClient := clientset.CoreV1().Services(apiv1.NamespaceDefault)

	watcher , err := serviceClient.Watch(context.TODO() , metav1.ListOptions{})
	if err != nil{
		panic(err)
	}

	ch := watcher.ResultChan()

	for event := range ch{

		svc , ok := event.Object.(*apiv1.Service)
		if !ok{
			fmt.Println("Not ok!")
		}

		switch event.Type{
		case watch.Deleted:
			fmt.Printf("Service Deleted %s\n" , svc.ObjectMeta.Name)

			switch svc.ObjectMeta.Name{
			case "gateway-service":
				createSerivce(clientset , gatewayService.servicePath)
			case "redis-service":
				createSerivce(clientset , gatewayService.dbservicePath)
			case "order-service":
				createSerivce(clientset , orderService.servicePath)
			case "mysql-service":
				createSerivce(clientset , orderService.dbservicePath)
			case "user-service":
				createSerivce(clientset , userService.servicePath)
			case "postgres-service":
				createSerivce(clientset , userService.dbservicePath)
			case "logistics-service":
				createSerivce(clientset , logisticsService.servicePath)
			case "logistics-postgres-service":
				createSerivce(clientset , logisticsService.dbservicePath)
			}
		
		case watch.Added:
			fmt.Println("Service created")
		}
	} 
}


/*
Watches for changes in status of deployment objects.
Creates a deployment object if gets a "Deleted" notification
*/
func watchDeployment(clientset *kubernetes.Clientset){
	deploymentClient := clientset.AppsV1().Deployments(apiv1.NamespaceDefault)

	watcher , err := deploymentClient.Watch(context.TODO() , metav1.ListOptions{})
	if err!=nil{
		panic(err)
	}
	ch := watcher.ResultChan()

	for event := range ch{
		dep , ok := event.Object.(*appsv1.Deployment)
		if !ok{
			fmt.Println("Deployment client could not be created !")
		}
		switch event.Type{
		case watch.Deleted:
			fmt.Printf("Deployment deleted %s\n" , dep.ObjectMeta.Name)

			switch dep.ObjectMeta.Name{
			case "gateway-deployment":
				createDeployment(clientset , gatewayService.deploymentPath)
			case "order-deployment":
				createDeployment(clientset , orderService.deploymentPath)
			case "user-deployment":
				createDeployment(clientset , userService.deploymentPath)
			case "logistics-deployment":
				createDeployment(clientset , logisticsService.deploymentPath)
			case "mysql-deployment":
				createDeployment(clientset , orderService.dbdeploymentPath)
			case "postgres-deployment":
				createDeployment(clientset , userService.dbdeploymentPath)
			case "postgres-logistics-deployment":
				createDeployment(clientset , logisticsService.dbdeploymentPath)
			}

		case watch.Added:
			fmt.Printf("Deployment object Added !! \n")
			// fmt.Printf("%v" , dep)
		}
	}
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

	go watchService(clientset)
	go watchDeployment(clientset)

	//Stops the main goroutine from exiting
	for ;;{

	}
	
}