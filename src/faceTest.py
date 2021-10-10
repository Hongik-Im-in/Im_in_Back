# importing libraries
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from torchvision import datasets
from torch.utils.data import DataLoader
from PIL import Image
import torchvision
import os

mtcnn = MTCNN(image_size=240, margin=0, min_face_size=20) # mtcnn 초기화
resnet = InceptionResnetV1(pretrained='vggface2').eval() # resnet을 pretrained된 것을 사용한다.

dataset=datasets.ImageFolder('./face') # 사진 폴더 경로
idx_to_class = {i:c for c,i in dataset.class_to_idx.items()} # folder내의 사진과 폴더명들을 각각 dict 형태로 저장

print(idx_to_class)


# def collate_fn(x):
#     return x[0]

# loader = DataLoader(dataset, collate_fn=collate_fn)

name_list = [] #target
embedding_list = [] # image cropped된 데이터들의 리스트


path = "./face"
file_list = os.listdir(path)


for i in range(0, 10):
    path_in = "./face/" + idx_to_class[i]
    file_list_in = os.listdir(path_in)
    for j in range(0, 10):
        img = Image.open("./face/" + idx_to_class[i] + "/" + file_list_in[j])
        img_cropped = mtcnn(img, save_path="./croppedFace/" + idx_to_class[i] + "/" + str(j+1) + ".jpg")

test_path = "./test/"
test_file_list = os.listdir(test_path)

for i in range(0, 10):
    img = Image.open("./test/" + test_file_list[i])
    img_cropped = mtcnn(img, save_path="./croppedTestFace/" + test_file_list[i])

dataset=datasets.ImageFolder('./croppedFace') # 사진 폴더 경로

def collate_fn(x):
    return x[0]

loader = DataLoader(dataset, collate_fn=collate_fn)

for img, idx in loader:
    face, prob = mtcnn(img, return_prob=True) 
    if face is not None and prob>0.90: # 얼굴이 탐지되고 확률 > 90% 이상일때
        emb = resnet(face.unsqueeze(0)) # passing cropped face into resnet model to get embedding matrix
        embedding_list.append(emb.detach()) # resulten embedding matrix is stored in a list
        name_list.append(idx_to_class[idx]) # 리스트에 저장된 이름


data = [embedding_list, name_list]
torch.save(data, 'golo.pt') # 모델 저장


def face_match(img_path, data_path): # img_path= 사진의 위치, data_path= 모델의 위치
    # 이미지 경로로 파일 불러오기
    img = Image.open(img_path)
    face, prob = mtcnn(img, return_prob=True) # 잘려진 얼굴과 확률을 리턴한다.
    
    emb = resnet(face.unsqueeze(0)).detach() # detach는 required grad를 false로 넘겨준다.
    
    saved_data = torch.load('golo.pt') # model 호출
    embedding_list = saved_data[0]
    

    name_list = saved_data[1] # 리스트에 있는 이름을 불러온다
    dist_list = [] # 각 인물사진과 test 사진 사이의 거리 값들을 저장하기 위한 리스트
    # 매치된 거리들, 거리중에 최소인 값을 
    for idx, emb_db in enumerate(embedding_list):
        dist = torch.dist(emb, emb_db).item()
        dist_list.append(dist)
    
    idx_min = dist_list.index(min(dist_list))
    return (name_list[idx_min], min(dist_list))

test_path = "./croppedTestFace/"
test_file_list = os.listdir(test_path)
# 모든 test 10명에 대한 결과 출력
for i in range(0, 9):
    path = './croppedTestFace/' + str(test_file_list[i]) #+'_test1.jpg'
    result = face_match(path, 'golo.pt')
    print("-----------------------------------------------------------\n", path)
    print('Face matched with: ',result[0], 'With distance: ',result[1], '\n')
    print("-----------------------------------------------------------\n")

