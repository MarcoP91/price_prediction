s3 = boto3.client('s3')
    
    in_mem_file = io.BytesIO()
    warp_rgb.warped_img.save(in_mem_file, format='jpeg')
    in_mem_file.seek(0)

    s3.upload_fileobj(in_mem_file, buck, f"test_inference_marco/{image_id}.jpg")

    response = client.invoke(
        FunctionName='arn:aws:lambda:eu-central-1:734849104975:function:SpotrInference-ils-streetview-materials-prd',
        InvocationType='RequestResponse',
        Payload=json.dumps({'bucket': buck, 'key':f"test_inference_marco/{image_id}.jpg"})
    )
    
    arr1, classmap = fetch_inferenced_segmentation_and_classmap(response)
  
  
  def fetch_inferenced_segmentation_and_classmap(response):
    response = response['Payload'].read()
    response = json.loads(response)
    classmap = json.loads(response['body'])['meta']['classmap']
    response = json.loads(response['body'])['result']
    
    return np.asarray(Image.open(BytesIO(base64.b64decode(response['segmentation'])))), classmap
  
  
  
