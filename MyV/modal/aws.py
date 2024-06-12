#aws에 파일 업로드하기
import os
import boto3
from .models import UploadAnalyzeFile
from django.conf import settings


def upload_to_s3(mySound_file, compareSound_file):
    ##파일 이름 변경##
    # 파일 이름에서 확장자 분리하기
    mySound_name, mySound_ext = os.path.splitext(mySound_file.name)
    compareSound_name, compareSound_ext = os.path.splitext(compareSound_file.name)    
    
    # 새 파일 이름 설정
    new_mySound_name = 'usr' + mySound_ext 
    new_compareSound_name = 'org' + compareSound_ext ##org.mp4 이런식으로 변경 
        
    mySound_file.name = new_mySound_name
    compareSound_file.name = new_compareSound_name
    #인스턴스 중복되는거 방지하기
    upload = UploadAnalyzeFile(mySound_file=mySound_file,
                               fMySound_name=mySound_file.name,
                               compareSound_file=compareSound_file, 
                               fCompareSound_name=compareSound_file.name)
    upload.save()


#aws에서 파일 다운로드하기
def downloadFile() :
    s3 = boto3.resource('s3')
    for bucket in s3.buckets.all():
        print(bucket.name)
    
    #s3 버킷 정보 가져오기
    bucket_name = 'myv-aws-bucket'
    bucket = s3.Bucket(bucket_name)
    print("###test###")
    print(bucket)

    #파일 다운로드 진행하기
    latest_upload = UploadAnalyzeFile.objects.latest('id')
    mine_file_name = latest_upload.fMySound_name
    print(mine_file_name)
    compare_file_name = latest_upload.fCompareSound_name
    print(compare_file_name)

    mine_obj_file = f'vocalReportSource/{mine_file_name}'
    compare_obj_file = f'vocalReportSource/{compare_file_name}'

    # 파일명 출력 테스트
    print("My sound file name:", mine_file_name)
    print("Compare sound file name:", compare_file_name)
    print("###버킷 접근 성공###")
    
    save_file = os.path.join(os.getcwd(), 'media', 'vocalReportSrc', mine_file_name) #저장위치 및 파일 다른 이름으로 저장하기 but 이름변경 안할거임
    bucket.download_file(mine_obj_file,save_file)

    save_file = os.path.join(os.getcwd(), 'media', 'vocalReportSrc', compare_file_name) #저장위치 및 파일 다른 이름으로 저장하기 but 이름변경 안할거임
    bucket.download_file(compare_obj_file,save_file)
    return 1;

#사용자마다 S3 디렉토리 버킷 생성하는 함수 (올리고, 다운받는 용도로 만든 후 음역대 저장하면 삭제할 함수)
def makingBucket():
    s3 = boto3.client('s3',
                  aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

    # 디렉토리 버킷 생성
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    userId='userid' #db 연결후 사용자 아이디로 디렉토리 버킷 만들 예정!
    directory_path = f'{userId}/'

    s3.put_object(Bucket=bucket_name, Key=(directory_path))
    return directory_path

#버킷 삭제
def deleteBucket(): #매개변수로 userId 받을 예정
    s3 = boto3.client('s3',
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    userId = 'userid'  # 매개변수로 받을 버킷 이름을 담을 예정
    directory_path = f'{userId}/'

    s3.delete_object(Bucket=bucket_name, Key=directory_path)