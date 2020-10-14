import boto3
import requests
import datetime
import time
import cv2

#Credentials----------------------------------------------------------------------------------
client = boto3.client('rekognition',
                      aws_access_key_id="ASIAZ6WXFO6Y7DTXJCUW",
                      aws_secret_access_key="7pl3sz9W9qL/ezC3XFpTESYK/FQrpbvOWKC0Tns/",
                      aws_session_token="FwoGZXIvYXdzEJX//////////wEaDAUV2T/DWkAgfEMVhCLDAcHUE7nR0RsndGfFtWsa/lOqEslQSsm8+CY5Z+P8v5nPHJWtseLXlZhXmu+ilPxAXd6IGHcAjFjCyf8MY30aKrdvNswlsv2seBxL+eqF+YBkJcQQFYnK7oqdGy22FGXclBOwgYuzuQhUNw0KcYHr9DdGwnRPn2v0CMy/3CNZZjmOr2f2D5SWP029zs7KmCQfleA2UblNaaj3rXr0El1sfz2COOT5kL7Z7lRRV/TuZtUrHsTIXnhJY511MURDvUiEh+B9mijpu5v8BTItx4kY2He/hMKpVESR9gNTowVKhUu5f1Z/USU5xO1Ps10oybOocow2mveE5L0E",
                      region_name='us-east-1')

#Capture images for every 1 hour and store the image with current date and time -----------------------------------------------------------------------------------
for j in range(0, 6):
    current_time = datetime.datetime.now().strftime("%d-%m-%y  %H-%M-%S ")
    print(current_time)
    camera = cv2.VideoCapture(0)
    for i in range(20):
        return_value, image = camera.read()
        if (i == 19):
            cv2.imwrite('Hourly Class Images/' + current_time + '.jpg', image)
    del (camera)

#Send the captured image to AWS S3 Bucket--------------------------------------------------------------------------------------
    clients3 = boto3.client('s3', region_name='us-east-1')
    clients3.upload_file("Hourly Class Images/"+current_time+'.jpg', 'add your S3 bucket name', current_time+'.jpg')

    #Recoginze students in captured image ---------------------------------------------------------------------------------------
    with open(r'Hourly Class Images/D.jpg','rb') as source_image:
        source_bytes = source_image.read()
    print(type(source_bytes))

    print("Recognition Service")
    response = client.detect_custom_labels(
        ProjectVersionArn='arn:aws:rekognition:us-east-1:684424787889:project/HourlyAttendance/version/HourlyAttendance.2020-10-07T17.13.07/1602070987758
        Image={
            'Bytes': source_bytes
        },

    )

    print(response)
    if not len(response['CustomLabels']):
         print('Not identified')

    else:
        str = response['CustomLabels'][0]['Name']
        print(str)
        # Update the attendance of recognized student in DynamoDB by calling the API
        url = " https://1f5t9pcbb2.execute-api.us-east-1.amazonaws.com/test?roll_number=" + str
        resp = requests.get(url)
        print(resp)
        if resp.status_code==200:
            print("Success")

    time.sleep(3600)