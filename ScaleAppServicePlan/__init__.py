import logging
import azure.functions as func
import requests
import os
import json

def get_managed_identity_token(resource="https://management.azure.com/"):
    url = "http://169.254.169.254/metadata/identity/oauth2/token"
    params = {
        "api-version": "2018-02-01",
        "resource": resource
    }
    headers = {
        "Metadata": "true"
    }
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()["access_token"]

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Requisição recebida para escalar App Service Plan.')

    subscription_id = os.getenv("SUBSCRIPTION_ID")
    resource_group = os.getenv("RESOURCE_GROUP")
    app_service_plan = os.getenv("APP_SERVICE_PLAN")
    new_instance_count = 3

    if not all([subscription_id, resource_group, app_service_plan]):
        return func.HttpResponse("Parâmetros de ambiente ausentes.", status_code=400)

    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Web/serverfarms/{app_service_plan}?api-version=2022-03-01"

    payload = {
        "sku": {
            "name": "S1",
            "tier": "Standard",
            "capacity": new_instance_count
        }
    }

    try:
        access_token = get_managed_identity_token()
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        response = requests.put(url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            logging.info("Escalamento realizado com sucesso.")
            return func.HttpResponse(f"Escalado para {new_instance_count} instâncias.", status_code=200)
        else:
            logging.error(f"Erro ao escalar: {response.text}")
            return func.HttpResponse("Falha ao escalar recurso.", status_code=500)

    except Exception as e:
        logging.error(f"Erro inesperado: {str(e)}")
        return func.HttpResponse("Erro interno na função.", status_code=500)
