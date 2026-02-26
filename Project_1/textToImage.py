import boto3
import json
import base64
import os

image_counter = 0

def textToImageFnc(prompt_data):
    global image_counter
    bedrock = boto3.client(service_name = "bedrock-runtime", region_name="us-west-2" )

    payload = {
        "prompt": prompt_data,
        "mode": "text-to-image",
        "output_format": "png",
        "aspect_ratio": "1:1"
    }

    body=json.dumps(payload)

    accept="application/json"
    content_type="application/json"
    model_id='stability.sd3-5-large-v1:0'

    response = bedrock.invoke_model(
        body=body,
        modelId=model_id,
        accept=accept,
        contentType=content_type,
    )
    raw_body = response["body"].read()
    response_body = json.loads(raw_body)
  
    if "images" in response_body and response_body["images"]:
        encoded_image = response_body["images"][0]
    else:
        raise RuntimeError(f"Unexpected response format: {response_body}")

    image_bytes = base64.b64decode(encoded_image)
    
    os.makedirs("static/trash", exist_ok=True)
    output_image_path = f"static/trash/{image_counter}.png"
    image_counter += 1

    with open(output_image_path, "wb") as image_file:
        image_file.write(image_bytes)

    return output_image_path
