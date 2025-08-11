# Azure Monitoring Autoscale Function 🚀

Este projeto contém uma Azure Function em Python que escala automaticamente um App Service Plan quando alertas críticos são detectados, utilizando Managed Identity para autenticação segura.

## 🔧 Componentes

- Azure Function (Python)
- Managed Identity
- Azure Monitor + Alerts
- Azure Logic Apps
- App Service Plan

## 🚀 Como funciona

1. Azure Monitor detecta uso excessivo de CPU
2. Logic App dispara a Azure Function
3. A função escala o App Service Plan para mais instâncias

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
                                    └──────────────────

## 📁 Estrutura

- `ScaleAppServicePlan/`: Código da função
- `logic-app-template/`: Template JSON do Logic App
- `requirements.txt`: Dependências Python

## 🔐 Segurança

Utiliza Managed Identity para autenticação com a API do Azure, evitando uso de credenciais explícitas.

## 🛠️ Configuração

Defina as seguintes variáveis de ambiente na Azure Function:

- `SUBSCRIPTION_ID`
- `RESOURCE_GROUP`
- `APP_SERVICE_PLAN`

## 📦 Deploy

Você pode publicar com Azure CLI, VS Code ou GitHub Actions.
