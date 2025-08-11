```markdown
# Azure Monitoring Autoscale Function 🚀

Este repositório contém uma solução completa para monitorar o uso de CPU de um App Service Plan no Microsoft Azure e escalar automaticamente o número de instâncias quando um limiar crítico for ultrapassado. A solução utiliza uma Azure Function em Python com Managed Identity para autenticação segura e um Logic App para orquestrar o fluxo de resposta.

---

## 📖 Visão Geral

A cada vez que o Azure Monitor detecta CPU acima de 90%, um alerta dispara um Logic App. O Logic App chama nossa Azure Function, que usa Managed Identity para autenticar na API REST do Azure e ajustar a capacidade do App Service Plan.

---

## 🏛️ Arquitetura

```plaintext
┌─────────────────┐       Alertas       ┌──────────────────┐
│ Azure Monitor   │ ──────────────────▶│ Azure Alerts     │
└─────────────────┘                     └──────────────────┘
                                             │
                                             ▼
                                    ┌──────────────────┐
                                    │ Azure Logic App  │
                                    │  - Trigger HTTP  │
                                    │  - Condição      │
                                    │  - Chama Function│
                                    └──────────────────┘
                                             │
                                             ▼
                                    ┌──────────────────┐
                                    │ Azure Function   │
                                    │  - HTTP Trigger  │
                                    │  - Managed ID    │
                                    │  - PUT REST API  │
                                    └──────────────────┘
                                             │
                                             ▼
                                    ┌──────────────────┐
                                    │ App Service Plan │
                                    │  - Sku Standard  │
                                    │  - Capacity N    │
                                    └──────────────────┘
```

---

## ⚙️ Componentes

- **Azure Function (Python)**  
  Código que autentica via Managed Identity e chama a API de escalonamento do Azure.

- **Managed Identity**  
  Identidade gerenciada atribuída à Function App para obter tokens sem credenciais embutidas.

- **Azure Monitor + Alerts**  
  Coleta métricas de CPU e dispara alertas quando os limiares são excedidos.

- **Azure Logic Apps**  
  Orquestra o fluxo de resposta: recebe o alerta e invoca a Azure Function.

- **App Service Plan**  
  Recurso de destino que terá seu número de instâncias ajustado.

---

## 📋 Pré-requisitos

- Conta ativa no Azure com permissão de Owner ou Contributor  
- [Azure CLI](https://docs.microsoft.com/cli/azure/install-azure-cli) (versão ≥ 2.0)  
- [Python 3.8+](https://www.python.org/downloads/)  
- [Azure Functions Core Tools](https://docs.microsoft.com/azure/azure-functions/functions-run-local)  
- [Git](https://git-scm.com/)  

---

## 🚀 Quick Start

1. Faça login no Azure:

   ```bash
   az login
   ```

2. Clone este repositório:

   ```bash
   git clone https://github.com/seu-usuario/azure-monitoring-autoscale.git
   cd azure-monitoring-autoscale
   ```

3. Instale dependências Python:

   ```bash
   pip install -r requirements.txt
   ```

4. Crie um Resource Group e um Storage Account para a Function:

   ```bash
   az group create --name rg-autoscale --location eastus
   az storage account create \
     --name stautoscale$RANDOM \
     --resource-group rg-autoscale \
     --sku Standard_LRS
   ```

5. Crie a Function App com Managed Identity:

   ```bash
   az functionapp create \
     --resource-group rg-autoscale \
     --consumption-plan-location eastus \
     --name func-autoscale \
     --storage-account stautoscale$RANDOM \
     --runtime python \
     --functions-version 3 \
     --assign-identity
   ```

6. Conceda à identidade da Function o papel Contributor no App Service Plan:

   ```bash
   # defina variáveis
   AZ_SUBSCRIPTION_ID=$(az account show --query id -o tsv)
   AZ_PRINCIPAL_ID=$(az functionapp identity show \
     --name func-autoscale \
     --resource-group rg-autoscale \
     --query principalId -o tsv)

   # atribua role
   az role assignment create \
     --assignee $AZ_PRINCIPAL_ID \
     --role Contributor \
     --scope /subscriptions/$AZ_SUBSCRIPTION_ID/resourceGroups/rg-autoscale/providers/Microsoft.Web/serverfarms/<SEU_PLAN_NAME>
   ```

7. Defina configurações de aplicação:

   ```bash
   az functionapp config appsettings set \
     --name func-autoscale \
     --resource-group rg-autoscale \
     --settings SUBSCRIPTION_ID=$AZ_SUBSCRIPTION_ID \
                RESOURCE_GROUP=rg-autoscale \
                APP_SERVICE_PLAN=<SEU_PLAN_NAME>
   ```

8. Faça deploy do código:

   ```bash
   func azure functionapp publish func-autoscale
   ```

9. Importe o Logic App:

   - No portal do Azure, crie um Logic App (Consumption).  
   - Em “Template de implantação”, escolha “Deploy a custom template” e cole o JSON em `logic-app-template/autoscale-logicapp.json`.  
   - Configure a URL de chamada para apontar à sua Function App.

---

## 🔍 Testando

1. Simule um alerta de CPU:

   ```bash
   # Exemplo de comando Kusto via Azure CLI
   az monitor metrics alert create \
     --name TesteCPUAlta \
     --resource-group rg-autoscale \
     --scopes /subscriptions/$AZ_SUBSCRIPTION_ID/resourceGroups/rg-autoscale/providers/Microsoft.Web/serverfarms/<SEU_PLAN_NAME> \
     --condition "avg Percentage CPU > 90" \
     --action "/subscriptions/$AZ_SUBSCRIPTION_ID/resourceGroups/rg-autoscale/providers/Microsoft.Logic/workflows/<SEU_LOGIC_APP>/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=<TOKEN>"
   ```

2. Verifique logs da Function:

   ```bash
   az functionapp log stream --name func-autoscale --resource-group rg-autoscale
   ```

3. Confira no portal do Logic Apps se a execução ocorreu e visualize as saídas.

---

## 🧹 Limpeza dos Recursos

Para evitar cobranças:

```bash
az group delete --name rg-autoscale --yes --no-wait
```

---

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

---

## 📜 Licença

MIT License © 2025 Douglas  

---
```
