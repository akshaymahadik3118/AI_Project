import boto3
import json 

def textToTextFnc(prompt_data):
    bedrock = boto3.client(service_name = "bedrock-runtime" , region_name="ap-south-1" )

    payload = {
        "anthropic_version": "bedrock-2023-05-31",
         "max_tokens": 200,
        "temperature": 0.7,
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt_data}]}],
    }

    body = json.dumps(payload)

    response = bedrock.invoke_model(
        body=body,
        modelId='arn:aws:bedrock:ap-south-1:345757498277:inference-profile/global.anthropic.claude-sonnet-4-5-20250929-v1:0',
        accept='application/json',
        contentType='application/json',
    )


    response_body = json.loads(response.get('body').read())
    parts = response_body.get("content", [])
    text = "".join(p.get("text", "") for p in parts if p.get("type") == "text")

    return text
    
