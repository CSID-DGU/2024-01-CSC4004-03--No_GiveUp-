from django.shortcuts import render
from django.http import HttpResponse
from .awsInMain import upload_to_s3,downloadFile
from .maxminAnalyze import maxminAnalyze
from .sportify_api import sportify
from .models import UserMaxMinNote
##QR
#pip install qrcode
import qrcode
import io, os
from django.core.files.base import ContentFile
from django.conf import settings

##async
from asgiref.sync import sync_to_async
import asyncio
##

def css(request):
    return render(request,'main/main_3.html')
def main_1(request):
    return render(request, 'main/main_1.html')

def upload_max_min(request):
    if request.method == 'POST':
        min_file = request.FILES.get('min_file', None)
        max_file = request.FILES.get('max_file', None)
        
        if min_file and max_file:
            user = request.user
            upload_to_s3(min_file, max_file, user)
            return HttpResponse("Files uploaded successfully")
        else:
            return HttpResponse("Failed to upload files")
    
    return HttpResponse("Failed to upload files")

def main_2(request):
    # user = request.user
    # # task1 = asyncio.ensure_future(maxminAnalyze(user))
    # # await asyncio.wait([task1])
    # maxminAnalyze(user)
    return render(request,'main/loading.html')

# def main_3(request):
#     user = request.user
#     #다시 추천 받을 때, 만약 최고음 최저음 분석을 한 번 했더라면 그냥 바로 디비 정보로 sportify만 돌리게하기 (리브로사 안쓰고!)
#     userNoteInfo = UserMaxMinNote.objects.filter(user=user).order_by('-id').first()  # 가장 마지막 정보만 가져오기

#     if userNoteInfo == None :
#         maxminAnalyze(user)
#     #song_names~preview_urls는 각각 리스트
#     #userInfo는 max,min, user_key_string, tmpo, energy 순으로 담긴 리스트
#     result = sportify(user)

#     if result[0]==1:
#         context = {
#             'user' : user,
#             'min' : result[2],
#             'max' : result[1],
#             'mood' : result[3],
#             'tmpo' : result[4],
#             'energy' : result[5],
#             'title1' : "추천된 곡이 없습니다.",
#             'title2' : "추천된 곡이 없습니다.",
#             'title3' : "추천된 곡이 없습니다.",
#             }

#         return render(request, 'main/main_3.html', context)
#     else :
#         song_names, song_urls, img_urls, preview_urls, artist, userInfo = sportify(user) 
        
#         # QR 코드 생성
#         url = request.build_absolute_uri()
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=10,
#             border=4,
#         )
#         qr.add_data(url)
#         qr.make(fit=True)
        
#         # QR 코드 이미지를 메모리 버퍼에 저장
#         img = qr.make_image(fill='black', back_color='white')
#         buffer = io.BytesIO()
#         img.save(buffer, format='PNG')
#         buffer.seek(0)
        
#         # QR 코드 이미지를 Django 저장소에 저장
#         qr_code_path = f'qr_codes/userId_{request.user.id}_qrcode.png'
#         qr_code_file = ContentFile(buffer.read(), qr_code_path)
#         media_path = os.path.join(os.getcwd(), 'media', qr_code_path)
#         with open(media_path,'wb') as f:
#             f.write(qr_code_file.read())
        
#         qr_code_url = media_path 
#         print("@##",qr_code_path,)
#         print("@##",qr_code_url)

#         # 템플릿에 전달할 컨텍스트에 QR 코드 이미지 URL 추가
#         context = {
#             'user': user,
#             'cover1': img_urls[0],
#             'cover2': img_urls[1],
#             'cover3': img_urls[2],
#             'title1': song_names[0],
#             'title2': song_names[1],
#             'title3': song_names[2],
#             'min': userInfo[1],
#             'max': userInfo[0],
#             'mood': userInfo[2],
#             'tmpo': userInfo[3],
#             'energy': userInfo[4],
#             'artist1': artist[0],
#             'artist2': artist[1],
#             'artist3': artist[2],
#             'preview1': preview_urls[0],
#             'preview2': preview_urls[1],
#             'preview3': preview_urls[2],
#             'qr_code_url': qr_code_url,
#         }
#         return render(request, 'main/main_3.html', context)

def main_3(request):
    user = request.user

    userNoteInfo = UserMaxMinNote.objects.filter(user=user).order_by('-id').first()

    if userNoteInfo is None:
        maxminAnalyze(user)

    result = sportify(user)

    if result[0] == 1:
        context = {
            'user': user,
            'min': result[2],
            'max': result[1],
            'mood': result[3],
            'tmpo': result[4],
            'energy': result[5],
            'title1': "추천된 곡이 없습니다.",
            'title2': "추천된 곡이 없습니다.",
            'title3': "추천된 곡이 없습니다.",
        }
        return render(request, 'main/main_3.html', context)
    else:
        song_names, song_urls, img_urls, preview_urls, artist, userInfo = sportify(user)
        
        # QR 코드 생성
        url = request.build_absolute_uri()
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # QR 코드 이미지를 메모리 버퍼에 저장
        img = qr.make_image(fill='black', back_color='white')
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # QR 코드 이미지를 media 디렉토리에 저장
        qr_code_path = f'qr_codes/userId_{request.user.id}_qrcode.png'
        media_path = os.path.join(settings.MEDIA_ROOT, qr_code_path)
        with open(media_path, 'wb') as f:
            f.write(buffer.read())
        
        # QR 코드 이미지 URL 생성
        qr_code_url = request.build_absolute_uri(settings.MEDIA_URL + qr_code_path)
        print("QR 코드 URL:", qr_code_url)
        print("########")
        print(os.path.join(settings.BASE_DIR, 'media')) 

        # 템플릿에 전달할 컨텍스트에 QR 코드 이미지 URL 추가
        context = {
            'user': user,
            'cover1': img_urls[0],
            'cover2': img_urls[1],
            'cover3': img_urls[2],
            'title1': song_names[0],
            'title2': song_names[1],
            'title3': song_names[2],
            'min': userInfo[1],
            'max': userInfo[0],
            'mood': userInfo[2],
            'tmpo': userInfo[3],
            'energy': userInfo[4],
            'artist1': artist[0],
            'artist2': artist[1],
            'artist3': artist[2],
            'preview1': preview_urls[0],
            'preview2': preview_urls[1],
            'preview3': preview_urls[2],
            'qr_code_url': qr_code_url,
        }
        return render(request, 'main/main_3.html', context)

#########test########
def qr(request):
    user = request.user
    sportify(user)
    return render(request, 'main/test.html')