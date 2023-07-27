# Basic and django imports 
import os
from django.conf import settings

# Rest Framework imports 
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

# Ml Model imports
from tensorflow.keras.models import load_model
from .predictions import predictBloodCancer

# Django Model imports 
from .models import ImageModel

# serializers imports 
from .serializers import ImageModelSerializer


class ImageModelViewSet(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageModelSerializer
    parser_classes = [MultiPartParser]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # config model name and Vertion
        model_name = 'blood_cancer_model'
        model_version = '1.0'
        model_extention = '.h5'

        # get and load the model
        full_model_name = model_name + "_v_" + model_version + model_extention
        model_path = os.path.join(
            settings.MEDIA_ROOT, 'models', full_model_name)
        try:
            # Load the model during Django app startup
            self.model = load_model(model_path)
            
            # load the model weights
            full_model_weights_name = "weights_"+full_model_name
            self.model.load_weights(weights_path)
            self.model.compile(optimizer='adamax', loss='categorical_crossentropy', metrics=['accuracy'])
        except Exception:
            self.model = None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Obtain the local storage path of the uploaded image
        image_path = serializer.instance.image.path

        if self.model:
            success = True
            # Perform prediction
            prediction_result = predictBloodCancer(image_path, self.model)

            # Get the instance of the created model
            instance = serializer.instance

            if prediction_result['is_cancer']:
                instance.description = 'The given sample is cancerous (leukemia).'
            else:
                instance.description = 'The given sample is non-cancerous.'
            instance.save()

            # Set the prediction_result field of the instance
            instance.prediction_result = prediction_result
            instance.save()
        else:
            success = False
            prediction_result = {}
            

        # Customize the response data
        response_data = {
            'success': success,
            'prediction_result': prediction_result
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
