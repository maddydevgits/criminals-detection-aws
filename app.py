import streamlit as st
import boto3
from PIL import Image
import os

accessKey='' # ask admin to share access key
secretAccessKey='' # ask admin to share secret access
region='us-east-1'

def load_image(img):
    return(Image.open(img))

st.title('Criminals Identification')

img_file=st.file_uploader('Upload Image',type=['png','jpg','jpeg'])

if img_file is not None:
    file_details={}
    file_details['name']=img_file.name
    file_details['type']=img_file.type
    file_details['size']=img_file.size
    st.write(file_details)

    st.image(load_image(img_file),width=250)

    with open(os.path.join('uploads','target.jpg'),'wb') as f:
        f.write(img_file.getbuffer())
    
    st.success('img saved')

    criminals_list=os.listdir('criminals')
    #st.write(criminals_list)
    client=boto3.client('rekognition',aws_access_key_id=accessKey,aws_secret_access_key=secretAccessKey,region_name=region)
    criminalFlag=0
    for i in criminals_list:
        imageSource=open('uploads/target.jpg','rb')
        targetSource=open('criminals/'+i,'rb')
        response=client.compare_faces(SimilarityThreshold=70,SourceImage={'Bytes':imageSource.read()},TargetImage={'Bytes':targetSource.read()})
        if response['FaceMatches']:
            criminalFlag=1
            result=i.split('.')[0]
            st.error('Criminal Identified as ' + result)
    else:
        if(criminalFlag==0):
            st.success('No Criminal Found')
