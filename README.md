# Startups Azure Migration Guide
The purpose of this guide is to get you the information you need for a successful migration to Azure.

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Startups Azure Migration Guide](#startups-azure-migration-guide)
- [Build Azure skills](#build-azure-skills)
- [Azure services documentation](#azure-services-documentation)
	- [AI and ML](#ai-and-ml)
	- [Infrastructure management and Automation](#infrastructure-management-and-automation)
	- [Data Engineering](#data-engineering)
	- [Compute](#compute)
	- [Databases](#databases)
	- [Containers](#containers)
	- [Internet of Things](#internet-of-things)
	- [Networking](#networking)
	- [Security](#security)
	- [Source management](#source-management)
	- [Storage](#storage)
	- [Testing / CI / CD](#testing-ci-cd)
	- [Web](#web)
	- [Blockchain](#blockchain)
- [Migrating from AWS?](#migrating-from-aws)

<!-- /TOC -->
## Build Azure skills
MS Learn provides [step-by-step guidance](https://docs.microsoft.com/en-us/learn/browse/?products=azure&resource_type=learning%20path) for using Azure services, including managing resources, creating serverless applications, managing security, and more.

## Azure services
Azure provides a very rich set of services that cover many different scenarios. Each service has extensive documentation, which include helpful resources, like quickstarts, tutorials, and samples.

### AI and ML
| Service                                                                                         | What it does |
| ----------------------------------------------------------------------------------------------  | ----  |
| [Cognitive Services](https://docs.microsoft.com/en-us/azure/cognitive-services/)                |       |
| [Machine Learning](https://docs.microsoft.com/en-us/azure/machine-learning/)                    |       |
| [Machine Learning Services](https://docs.microsoft.com/en-us/azure/machine-learning/service)    |       |
| [Machine Learning Studio](https://docs.microsoft.com/en-us/azure/machine-learning/studio)       |       |
| [Azure Bot Service](https://docs.microsoft.com/bot-framework/bot-service-overview-introduction) |       |
| [Azure Cognitive Search](https://docs.microsoft.com/en-us/azure/search/)                        |       |
| [Open Datasets](https://docs.microsoft.com/en-us/azure/open-datasets)                           |       |



### Infrastructure management and Automation
| Service                                                                                         | What it does |
| ----------------------------------------------------------------------------------------------  | ----  |
| [App Configuration](https://docs.microsoft.com/en-us/azure/azure-app-configuration/) | |
| [Application Insights](https://docs.microsoft.com/en-us/azure/application-insights/) | |
| [Scheduler](https://docs.microsoft.com/en-us/azure/scheduler/) | |
| [Automation](https://docs.microsoft.com/en-us/azure/automation/) | |
| [Azure Monitor](https://docs.microsoft.com/en-us/azure/monitoring-and-diagnostics/) | |
| [Azure Resource Manager](https://docs.microsoft.com/en-us/azure/azure-resource-manager/) | |
| [Azure Blueprints](https://docs.microsoft.com/en-us/azure/governance/blueprints/) | |
| [CLI](https://docs.microsoft.com/en-us/azure/cli/index) | Access Azure directly from the command-line. |
| [SDK](https://docs.microsoft.com/en-us/azure/sdks/index) | |
| [Cloud Shell](https://docs.microsoft.com/en-us/azure/cloud-shell/overview) | |

### Data Engineering
| Service                                                                                         | What it does |
| ----------------------------------------------------------------------------------------------  | ----  |
| [Azure Databricks](https://docs.microsoft.com/en-us/azure/azure-databricks/) | |
| [Azure HDInsight](https://docs.microsoft.com/en-us/azure/hdinsight/) | |
| [Apache Spark](https://docs.microsoft.com/en-us/azure/hdinsight/spark/apache-spark-overview) | |
| [Apache Storm](https://docs.microsoft.com/en-us/azure/hdinsight/storm/apache-storm-overview) | |
| [Azure Data Explorer](https://docs.microsoft.com/en-us/azure/data-explorer/) | |
| [Stream Analytics](https://docs.microsoft.com/en-us/azure/stream-analytics/) | |
| [Event Hubs](https://docs.microsoft.com/en-us/azure/event-hubs/) | |

### Compute
| Service                                                                                         | What it does |
| ----------------------------------------------------------------------------------------------  | ----  |
| [App Service](https://docs.microsoft.com/en-us/azure/app-service/) | |
| [Batch](https://docs.microsoft.com/en-us/azure/batch/) | |
| [Cloud Services]() | |
| [Functions](https://docs.microsoft.com/en-us/azure/azure-functions/) | |
| [Linux VM](https://docs.microsoft.com/en-us/azure/virtual-machines/linux/) | |
| [Windows VM](https://docs.microsoft.com/en-us/azure/virtual-machines/windows/) | |

### Databases
| Service                                                                                         | What it does |
| ----------------------------------------------------------------------------------------------  | ----  |
| [Azure SQL Database](https://docs.microsoft.com/en-us/azure/sql-database/) | |
| [CosmosDB](https://docs.microsoft.com/en-us/azure/cosmos-db/) | |
| [Data Factory](https://docs.microsoft.com/en-us/azure/data-factory/) | |
| [Azure Cache for Redis](https://docs.microsoft.com/en-us/azure/azure-cache-for-redis/) | |
| [Table Storage](https://docs.microsoft.com/en-us/azure/cosmos-db/table-storage-overview) | |
| [Azure Database for PostreSQL](https://docs.microsoft.com/en-us/azure/postgresql/) | |
| [Azure Database for MySQL](https://docs.microsoft.com/en-us/azure/mysql/) | |
| [Azure Database Migration Service](https://docs.microsoft.com/en-us/azure/dms/dms-overview) | |

### Containers
| Service                                                                                         | What it does |
| ----------------------------------------------------------------------------------------------  | ----  |
| [Azure Kubernetes Service (AKS)](https://docs.microsoft.com/en-us/azure/aks/) | |
| [Container Instances](https://docs.microsoft.com/en-us/azure/container-instances/) | |
| [Azure Container Registry](https://docs.microsoft.com/en-us/azure/container-registry/) | |
| [Web App for Containers](https://docs.microsoft.com/en-us/azure/app-service/containers/) | |

### Internet of Things
| Service                                                                                         | What it does |
| ----------------------------------------------------------------------------------------------  | ----  |
| [IoT Hub](https://docs.microsoft.com/en-us/azure/iot-hub/) | |
| [IoT Edge](https://docs.microsoft.com/en-us/azure/iot-edge/) | |
| [Azure Sphere](https://docs.microsoft.com/en-us/azure-sphere/) | |

### Networking
| Service                                                                                         | What it does |
| ----------------------------------------------------------------------------------------------  | ----  |
| [Traffic Manager](https://docs.microsoft.com/en-us/azure/traffic-manager/) | |
| [Load Balancer](https://docs.microsoft.com/en-us/azure/load-balancer/) | |
| [Azure Front Door Service](https://docs.microsoft.com/en-us/azure/frontdoor/) | |

### Security
| Service                                                                                         | What it does |
| ----------------------------------------------------------------------------------------------  | ----  |
| [Key Vault](https://docs.microsoft.com/en-us/azure/key-vault/) | |
| [Application Gateway](https://docs.microsoft.com/en-us/azure/application-gateway/) | |
| [Azure Firewall](https://docs.microsoft.com/en-us/azure/firewall/) | |
| [Azure DDoS Protection](https://docs.microsoft.com/en-us/azure/virtual-network/ddos-protection-overview) | |

### Source management
| Service                                                                                         | What it does |
| ----------------------------------------------------------------------------------------------  | ----  |
| [Azure DevOps](https://docs.microsoft.com/en-us/azure/devops/) | |
| [GitHub](https://github.com/) | |

### Storage
| Service                                                                                         | What it does |
| ----------------------------------------------------------------------------------------------  | ----  |
| [Storage](https://docs.microsoft.com/en-us/azure/storage/) | |
| [Blob Storage](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction/) | |
| [Disk Storage](https://docs.microsoft.com/en-us/azure/virtual-machines/windows/managed-disks-overview) | |
| [Managed Disks](https://docs.microsoft.com/en-us/azure/virtual-machines/windows/managed-disks-overview) | |
| [Queue Storage](https://docs.microsoft.com/en-us/azure/storage/queues/storage-queues-introduction/) | |

### Testing / CI / CD
| Service                                                                                         | What it does |
| ----------------------------------------------------------------------------------------------  | ----  |
| [Azure Lab Services](https://docs.microsoft.com/en-us/azure/lab-services/) | |
| [Azure DevOps Projects](https://docs.microsoft.com/en-us/azure/devops-project) | |
| [Azure Dev Spaces](https://docs.microsoft.com/en-us/azure/dev-spaces/) | |

### Web
| Service                                                                                         | What it does |
| ----------------------------------------------------------------------------------------------  | ----  |
| [App Service - Web Apps](https://docs.microsoft.com/en-us/azure/app-service-web) | |
| [Azure SignalR Service](https://docs.microsoft.com/en-us/azure/azure-signalr) | |
| [API Apps](https://docs.microsoft.com/en-us/azure/app-service-api) | |

### Blockchain
| Service                                                                                         | What it does |
| ----------------------------------------------------------------------------------------------  | ----  |
| [Azure Blockchain Service](https://docs.microsoft.com/en-us/azure/blockchain/service/) | |
| [Azure Blockchain Workbench](https://docs.microsoft.com/en-us/azure/blockchain/workbench/) | |


## Migrating from AWS?
Here is a comparison of the services on AWS and Azure. https://docs.microsoft.com/en-us/azure/architecture/aws-professional/services
