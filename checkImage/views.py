# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# #from snippets.models import Snippet
# #from snippets.serializers import SnippetSerializer
# from checkImage.models import checkImage
# from checkImage.serializers import CheckSerializer
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework import permissions
# import os
# from PIL import Image
# from facenet_pytorch import MTCNN, InceptionResnetV1


# @api_view(['GET', 'POST'])
# @permission_classes((permissions.AllowAny,))
# def check_list(request, format=None):
#     if request.method == 'GET':
#         images = checkImage.objects.all()
#         serializer = CheckSerializer(images, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = CheckSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()

#             mtcnn = MTCNN(image_size=240, margin=0, min_face_size=20) # mtcnn 초기화


#             path_in = "./media/check/"
#             file_list_in = os.listdir(path_in)
            
#             print(file_list_in)

#             for i in range(len(file_list_in)):
#                 path = "./media/croppedCheck/" + file_list_in[i] + '/'
#                 img = Image.open("./media/check/" + file_list_in[i])
#                 img_cropped = mtcnn(img, save_path= path + file_list_in[i])

#             new_path = './media/croppedCheck/'
#             folder_list = os.listdir(new_path)
#             print(folder_list)

#             # cnt = 0
#             # for i in file_list:
#             #     cnt += 1
#             #     data_path = new_path + i[:7] + '/'
#             #     for j in folder_list:
#             #         if i[:7] == j:
#             #             os.replace(path + i, data_path + i[:7] + '_' + str(cnt) + '.jpg')


#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
#from snippets.models import Snippet
#from snippets.serializers import SnippetSerializer
from checkImage.models import checkImage
from checkImage.serializers import CheckSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

from django.http import JsonResponse
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from torchvision import datasets
from torch.utils.data import DataLoader
from PIL import Image
import torchvision
import os
import time


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def check_list(request, format=None):
    if request.method == 'GET':
        images = checkImage.objects.all()
        serializer = CheckSerializer(images, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CheckSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            ## 폴더 생성

            ## 체크
            mtcnn = MTCNN(image_size=240, margin=0, min_face_size=20)  # initializing mtcnn for face detection
            resnet = InceptionResnetV1(pretrained='vggface2').eval()  # initializing resnet for face img to embeding conversion

            path = "media/check/b123456"
            file_list = os.listdir(path)
            img = Image.open("media/check/b123456/" + file_list[0])
            time.sleep(3)
            print("sleep1")
            #img = img.transpose(Image.ROTATE_270)
            img_cropped = mtcnn(img, save_path="media/croppedCheck/b123456/"+"cropped_b123456"+".jpg")
            time.sleep(3)
            print("sleep2")

            def face_match(img_path, data_path):  # img_path= location of photo, data_path= location of data.pt
                # getting embedding matrix of the given img
                img = Image.open(img_path)
                face, prob = mtcnn(img, return_prob=True)  # returns cropped face and probability
                emb = resnet(face.unsqueeze(0)).detach()  # detech is to make required gradient false

                saved_data = torch.load(data_path)  # loading data.pt file
                #print(saved_data)
                embedding_list = saved_data[0]  # getting embedding data
                name_list = saved_data[1]  # getting list of names
                dist_list = []  # list of matched distances, minimum distance is used to identify the person

                for idx, emb_db in enumerate(embedding_list):
                    dist = torch.dist(emb, emb_db).item()
                    dist_list.append(dist)

                # print(len(embedding_list))
                # print(embedding_list[0].shape)
                # print(type(embedding_list[0]))

                idx_min = dist_list.index(min(dist_list))
                return (name_list[idx_min], min(dist_list))

            result = face_match('media/croppedCheck/b123456/cropped_b123456.jpg', 'golo.pt')
            print(result)
            dummy_data = {
                "title": "student check",
                "description": "dd",
                "check_list": [
                    { "id": result[0], "studentId": "b123456", "check": result[1] },
                    { "id": "test id", "studentId": "test student id", "check": "test check" },
                ]
            }
            # 삭제

            return JsonResponse(dummy_data, status=status.HTTP_201_CREATED)
            #return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)