from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
#from snippets.models import Snippet
#from snippets.serializers import SnippetSerializer
from getImage.models import Image
from getImage.serializers import ImageSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
import os

@api_view(['GET', 'PUT','POST'])
@permission_classes((permissions.AllowAny,))
def image_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            ## 폴더 생성
            sid = request.data.get('title')

            ## 체크
            mtcnn = MTCNN(image_size=240, margin=0, min_face_size=20)  # initializing mtcnn for face detection
            resnet = InceptionResnetV1(pretrained='vggface2').eval()  # initializing resnet for face img to embeding conversion
            
            start = time.time()

            print("checkpoint 0")
           
            path = "media/check/"+sid
            file_list = os.listdir(path)
            img = Image.open(path + "/" + file_list[0])
                
            print("checkpoint 1:", time.time() - start)
            img_cropped = mtcnn(img, save_path="media/croppedCheck/"+sid+"/cropped_"+sid+".jpg") 
            print("checkpoint 2:", time.time() - start)
            
            
            
           

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

            print("checkpoint 3:", time.time() - start)
            result = face_match("media/croppedCheck/"+sid+"/cropped_"+sid+".jpg", 'golo.pt')
            print("checkpoint 4:", time.time() - start)

            print(result)

            checked = False
            if sid == result[0]:
                checked = True
                
            dummy_data = {
                "title": "student check",
                "description": "dd",
                "check_list": [
                    { "id": sid, "check": checked },
                ]
            }
            # 삭제
            print("checkpoint 5:", time.time() - start)
            # 특정 폴더내의 사진 삭제하기.
            dir_name = 'media/croppedCheck'
            list_dir = os.listdir(dir_name)
            for item in list_dir:
                if item.endswith(".jpg") or item.endswith(".png"):
                    os.remove(os.path.join(dir_name, item))

            return JsonResponse(dummy_data, status=status.HTTP_201_CREATED)
            #return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT','POST'])
@permission_classes((permissions.AllowAny,))
def attendance_list(request, format=None):
    