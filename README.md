# Azure Monitoring Autoscale Function 🚀

Este projeto implementa uma solução de escalonamento automático para Azure App Service Plans, acionada por alertas do Azure Monitor e orquestrada por um Azure Logic App. A autenticação segura com a API do Azure é realizada através de Managed Identity.

## ✨ Funcionalidades Detalhadas

- **Escalabilidade Responsiva:** A função ajusta dinamicamente o número de instâncias do App Service Plan em resposta a picos de carga detectados pelo Azure Monitor.
- **Autenticação Baseada em Identidade:** Utiliza Managed Identity atribuída à Azure Function para interagir com a API do Azure, eliminando a necessidade de armazenar e gerenciar segredos.
- **Fluxo de Automação com Logic Apps:** O Azure Logic App atua como um intermediário, recebendo alertas do Azure Monitor e acionando a Azure Function via HTTP.
- **Limites de Escalonamento Configuráveis:** O código da função inclui um limite máximo para o número de workers, protegendo contra escalonamento excessivo.
- **Estrutura de Projeto Padrão:** Organizado de acordo com as convenções de projetos de Azure Functions para facilitar o desenvolvimento e o deploy.

## 🔧 Componentes Utilizados

- **Azure Function (Python):** Contém a lógica principal para obter o estado atual do App Service Plan e solicitar o escalonamento.
- **Managed Identity:** Um recurso de identidade no Azure AD associado à Azure Function, utilizado para autenticação.
- **Azure Monitor + Regras de Alerta:** Configurado para monitorar métricas relevantes (ex: CPU, memória) e disparar alertas quando os limites são excedidos.
- **Azure Logic Apps:** Um serviço de fluxo de trabalho sem servidor que recebe alertas do Azure Monitor e chama a Azure Function.
- **Azure App Service Plan:** O plano de hospedagem que será escalado.

## 🚀 Como Funciona o Fluxo

1. **Configuração do Azure Monitor:** Você configura regras de alerta no Azure Monitor para o seu App Service Plan, baseadas em métricas como uso de CPU, memória, etc.
2. **Configuração do Logic App:** Cria-se um Azure Logic App com um gatilho HTTP que será acionado pelo alerta do Azure Monitor. Este Logic App contém uma ação para chamar a URL da Azure Function.
3. **Configuração da Azure Function:** A Azure Function é configurada com uma Managed Identity e variáveis de ambiente para identificar a assinatura, grupo de recursos e nome do App Service Plan.
4. **Disparo do Alerta:** Quando uma métrica monitorada atinge o limite definido, o Azure Monitor dispara o alerta.
5. **Acionamento do Logic App:** O alerta do Azure Monitor envia uma requisição HTTP para a URL do gatilho do Logic App.
6. **Chamada da Azure Function:** O Logic App executa sua ação HTTP, chamando a Azure Function.
7. **Execução da Lógica de Escala:** A Azure Function autentica-se na API do Azure usando sua Managed Identity, obtém o estado atual do App Service Plan e, se o limite máximo não foi atingido, solicita o aumento do número de workers.
8. **Escalonamento do App Service Plan:** O Azure processa a solicitação da Azure Function e escala o App Service Plan.

## 📁 Estrutura do Projeto

- `ScaleAppServicePlan/`: Contém o código Python (`__init__.py`) e o arquivo de configuração (`function.json`) da Azure Function.
- `logic-app-template/`: Contém o template JSON (`autoscale-logicapp.json`) para implantação do Azure Logic App.
- `requirements.txt`: Lista as dependências Python necessárias para a Azure Function.
- `host.json`: Arquivo de configuração global para a Azure Function App.
- `.gitignore`: Especifica arquivos e diretórios a serem ignorados pelo Git.
- `readme.md`: Este arquivo, fornecendo uma visão geral do projeto.

## 🔐 Segurança: Managed Identity

A Managed Identity é a abordagem recomendada para autenticação em serviços Azure. Em vez de usar chaves de acesso ou senhas, a Azure Function recebe uma identidade gerenciada automaticamente pelo Azure AD. Você concede permissões a essa identidade (por exemplo, permissões para gerenciar App Service Plans) e a Azure Function a utiliza para se autenticar na API do Azure. Isso reduz o risco de vazamento de credenciais.

## 🛠️ Configuração da Azure Function

Para que a Azure Function funcione corretamente, as seguintes variáveis de ambiente devem ser definidas no Azure Function App após a implantação:

- `SUBSCRIPTION_ID`: O ID da sua assinatura Azure.
- `RESOURCE_GROUP`: O nome do grupo de recursos onde o App Service Plan está localizado.
- `APP_SERVICE_PLAN`: O nome do App Service Plan a ser escalado.

Além disso, a Managed Identity da Azure Function deve ter permissões para realizar a operação de escrita (`Microsoft.Web/serverfarms/write`) no App Service Plan alvo.

## 📦 Deploy

Você pode implantar este projeto no Azure de várias maneiras:

1. **Azure CLI:** Utilize comandos `az functionapp deploy` para publicar a Azure Function e `az deployment group create` com o template do Logic App.
2. **VS Code Azure Functions Extension:** A extensão facilita a publicação direta do código da função.
3. **GitHub Actions:** Configure um workflow de CI/CD para implantar automaticamente a Azure Function e o Logic App a partir do seu repositório GitHub.

**Passos Gerais de Deploy:**

1. Crie um Azure Function App no Azure.
2. Habilite a Managed Identity para o Azure Function App.
3. Atribua as permissões necessárias à Managed Identity no nível do Resource Group ou App Service Plan.
4. Defina as variáveis de ambiente (`SUBSCRIPTION_ID`, `RESOURCE_GROUP`, `APP_SERVICE_PLAN`) no Azure Function App.
5. Implante o código da Azure Function no Function App.
6. Implante o Azure Logic App usando o template fornecido, configurando a URL da Azure Function.
7. Configure as regras de alerta no Azure Monitor para acionar o Logic App.

## Contribuições

Sinta-se à vontade para contribuir com melhorias e sugestões!

## Licença

📜 Licença
MIT License © 2025 Douglas
