import boto3
import json 

def textToTextFnc(prompt_data):
    bedrock = boto3.client(service_name = "bedrock-runtime" , region_name="ap-south-1" )

    payload = {
        "prompt":f"\n\nHuman:{prompt_data}\n\nAssistant:",
        "max_tokens_to_sample":512,
        "temperature":0.8,
        "top_p":0.8,
    }

    body = json.dumps(payload)

    response = bedrock.invoke_model(
        body=body,
        modelId='amazon.titan-text-express-v1',
        accept='application/json',
        contentType='application/json',
    )


    response_body = json.loads(response.get('body').read())
    return response_body.get('completion')
