from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import ImageModel
from .serializers import ImageModelSerializer


class ImageModelViewSet(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageModelSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Customize the response data
        image_url = serializer.data['image']
        response_data = {
            'message': 'Image uploaded successfully.',
            'image_url': request.build_absolute_uri(image_url)
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
