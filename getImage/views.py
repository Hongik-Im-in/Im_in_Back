from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
#from snippets.models import Snippet
#from snippets.serializers import SnippetSerializer
from getImage.models import Image
from getImage.serializers import ImageSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def image_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
