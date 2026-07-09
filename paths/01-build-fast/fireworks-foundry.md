# Deploy and serve Fireworks models natively on Microsoft Foundry 
 
*A reference architecture for AI-native startups* 
 
This page demonstrates the shortest path to run an Azure-hosted application that calls a Fireworks AI model deployed through Microsoft Foundry.  
 
## What you build 
 
- A Fireworks model deployment in Microsoft Foundry. 
- A minimal Python Flask app that calls the Fireworks deployment endpoint. 
- An Azure Container Registry image for the app. 
- An Azure Container Apps service that runs the image and exposes `/` and `/chat` endpoints. 
- A Container Apps secret for the Fireworks key, referenced by an environment variable. 
- Basic validation steps so you know the app and the Fireworks call both work. 
 
## Before you begin, you'll need:
 
- An Azure subscription. 
- A Microsoft Foundry resource and project. 
- Permission to deploy models in Foundry. 
- Permission to create Azure Container Apps and Azure Container Registry resources. 
- Azure CLI installed and signed in to the correct subscription. 
- A local editor such as Visual Studio Code. 
 
Before running Azure CLI commands, verify your CLI account and subscription: 
 
```bash 
az account show --output table 
az account list --output table 
az account set --subscription "<subscription-name-or-id>" 
``` 
The account used by the Visual Studio Code Azure extension may not be the same account used by Azure CLI in the terminal. 
 
### 1. Deploy a Fireworks model in Microsoft Foundry 
 
1. Open the [Microsoft Foundry portal](https://ai.azure.com/) and create or select a project. 
2. Open the model catalog, filter by publisher Fireworks AI, and choose the model you want to use. 
3. Select the deployment option that fits your workload: Data Zone Standard / per-token for prototypes and variable traffic, or Global provisioned throughput for predictable production workloads that need reserved capacity and more consistent performance. 
4. Deploy the model and wait until the deployment status is Succeeded. 
5. From the deployment details page, copy the Target URI, endpoint key, and deployment name. You will pass these values to the container app as environment variables or Container Apps secrets. 
 
Fireworks model availability depends on the Foundry resource region, selected model, and deployment type or offer. If you see an Unsupported Region error, confirm those three values and retry if the configuration looks valid before recreating the project. 

### 2. Store endpoint settings 
 
For a quick prototype, use Container Apps secrets. For a shared or production-like environment, store the key in Key Vault and grant the app identity permission to read it. The tested quickstart path uses Container Apps secrets. 
 
```text 
FIREWORKS_ENDPOINT=<base-model-endpoint> 
FIREWORKS_KEY=<endpoint-key> 
FIREWORKS_DEPLOYMENT=<deployment-name> 
``` 
 
If the Fireworks deployment Target URI looks like this: 
 
```text 
https://<resource>.services.ai.azure.com/models/chat/completions?api-version=2024-05-01-preview 
``` 
 
Use only the base model endpoint for FIREWORKS_ENDPOINT: 
 
```text 
https://<resource>.services.ai.azure.com/models 
``` 
 
Use the deployment name from the Foundry Deployments page for FIREWORKS_DEPLOYMENT. The deployment name may differ from the model display name in the catalog. 
 
### 3. Create a minimal sample app 
 
If you do not already have a containerized app, create a new local folder, such as `fw-chat`, and add three files: `app.py`, `requirements.txt`, and `Dockerfile`. 
 
#### app.py 
 
```python 
import os 
 
from azure.ai.inference import ChatCompletionsClient 
from azure.ai.inference.models import SystemMessage, UserMessage 
from azure.core.credentials import AzureKeyCredential 
from flask import Flask, jsonify, request 
 
app = Flask(__name__) 
 
 
@app.get("/") 
def health(): 
   return jsonify({"status": "ok"}) 
 
 
@app.post("/chat") 
def chat(): 
   client = ChatCompletionsClient( 
       endpoint=os.environ["FIREWORKS_ENDPOINT"], 
       credential=AzureKeyCredential(os.environ["FIREWORKS_KEY"]), 
   ) 
 
   body = request.get_json(silent=True) or {} 
   prompt = body.get("prompt", "Write one sentence about Fireworks on Foundry.") 
 
   response = client.complete( 
       model=os.environ["FIREWORKS_DEPLOYMENT"], 
       messages=[ 
           SystemMessage(content="You are a helpful assistant."), 
           UserMessage(content=prompt), 
       ], 
       temperature=0.2, 
       max_tokens=512, 
   ) 
 
   return jsonify({"response": response.choices[0].message.content}) 
 
 
if __name__ == "__main__": 
   app.run(host="0.0.0.0", port=8080) 
``` 

#### requirements.txt 
 
```text 
flask 
gunicorn 
azure-ai-inference 
azure-core 
``` 
 
#### Dockerfile 
 
```dockerfile 
FROM python:3.12-slim 
 
WORKDIR /app 
 
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt 
 
COPY app.py . 
 
EXPOSE 8080 
 
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"] 
``` 
 
### 4. Create or choose an Azure Container Registry 
 
Before creating the Container App, you need a container image in a registry that Azure Container Apps can pull from. Use Azure Container Registry for the simplest Azure-native path. 
 
If you do not already have a registry, see [Create an Azure Container Registry using the portal](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-get-started-portal). 
 
### 5. Build and push the image to Azure Container Registry 
 
From the folder that contains `app.py`, `requirements.txt`, and `Dockerfile`, run: 
 
```bash 
az acr build --registry <acr-name> --image fw-chat:latest --file Dockerfile . 
``` 
 
Use the registry name only, such as `fwreg`, not the full login server `fwreg.azurecr.io`. After the build completes, confirm that the repository and tag appear in Azure Container Registry: 
 
```text 
Repository: fw-chat 
Tag: latest 
``` 
 
For more detail, see [Build and push a container image using ACR Tasks](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-tutorial-quick-task). 
 
### 6. Create the Container App 
 
Create a Container Apps environment during Container App creation in the Azure portal, or create it ahead of time with Azure CLI: 
 
```bash 
az containerapp env create --name fw-env --resource-group <resource-group> --location <region> 
``` 
 
When the portal asks for container image settings, use the image you pushed to Azure Container Registry: 
 
```text 
Registry: <acr-name>.azurecr.io 
Image: fw-chat 
Tag: latest 
Target port: 8080 
Ingress: External 
``` 

### 7. Configure secrets and environment variables 
 
Store the Fireworks deployment key as a Container Apps secret, then reference that secret from the FIREWORKS_KEY environment variable. 
 
```powershell 
az containerapp secret set ` 
 --name fw-chat ` 
 --resource-group <resource-group> ` 
 --secrets fireworks-key="<fireworks-deployment-key>" 
``` 
 
Set the environment variables in the container app: 
 
```powershell 
az containerapp update ` 
 --name fw-chat ` 
 --resource-group <resource-group> ` 
 --set-env-vars ` 
   "FIREWORKS_ENDPOINT=https://<resource>.services.ai.azure.com/models" ` 
   "FIREWORKS_DEPLOYMENT=<deployment-name>" ` 
   "FIREWORKS_KEY=secretref:fireworks-key" 
``` 
 
Verify that the active container template has the expected environment variable shape: 
 
```powershell 
az containerapp show ` 
 --name fw-chat ` 
 --resource-group <resource-group> ` 
 --query "properties.template.containers[0].env" ` 
 -o json 
``` 
 
```json 
[ 
 { 
   "name": "FIREWORKS_ENDPOINT", 
   "value": "https://<resource>.services.ai.azure.com/models" 
 }, 
 { 
   "name": "FIREWORKS_DEPLOYMENT", 
   "value": "<deployment-name>" 
 }, 
 { 
   "name": "FIREWORKS_KEY", 
   "secretRef": "fireworks-key" 
 } 
] 
``` 
 
### 8. Validate the deployment 
 
Get the Container App URL: 
 
```powershell 
$appUrl = az containerapp show ` 
 --name fw-chat ` 
 --resource-group <resource-group> ` 
 --query "properties.configuration.ingress.fqdn" ` 
 -o tsv 
``` 
 
Test the health endpoint: 
 
```powershell 
Invoke-RestMethod -Uri "https://$appUrl/" 
``` 
 
Expected response: 
 
```json 
{"status":"ok"} 
``` 
 
Test the chat endpoint: 
 
```powershell 
Invoke-RestMethod ` 
 -Uri "https://$appUrl/chat" ` 
 -Method POST ` 
 -ContentType "application/json" ` 
 -Body '{"prompt":"Write one sentence about Fireworks on Foundry."}' 
``` 


## Troubleshooting 
 
| Issue | What to check | 
|---|---| 
| Unsupported Region | Confirm the Foundry resource region, selected model, and deployment type. Refresh and retry if the configuration looks valid. | 
| Missing expression after unary operator -- | You are probably running a Bash-style multi-line command in PowerShell. Use PowerShell line continuations or run the command on one line. | 
| ACR build fails with unexpected dockerfile format | Confirm the file is named exactly Dockerfile, with no extension, and starts with FROM. | 
| Container App activation fails | Check Revisions and replicas, then Log stream. Confirm the app listens on 0.0.0.0:8080. | 
| /chat fails with KeyError: FIREWORKS_KEY | Confirm that the Container Apps secret exists and that the active revision has FIREWORKS_KEY set as secretRef: fireworks-key. | 
| /chat returns 401 | Confirm that FIREWORKS_ENDPOINT is the base /models endpoint, not the Foundry project endpoint and not the full /chat/completions Target URI. Confirm the deployment key is current. | 
