from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import SoilData, Land, CropsData
from .serializers import SoilDataSerializer, LandSerializer, FarmerSerializer
from .utils import SubtractionMatrix,getCropsSuggestion
from django.shortcuts import render

def index(request):
    return render(request,'index.html',)

def service(request):
    return render(request,'service.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

class SoilDataView(APIView):
    def get(self, request):
        try:
            soil_data_objects = SoilData.objects.filter(land=request.query_params.get('land')).order_by('-time')
            serializer = SoilDataSerializer(soil_data_objects, many=True)
            return Response(serializer.data)
        except:
            return Response({'success': False, 'message': 'land not found!', 'status': 404}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = SoilDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CropsSuggestionView(APIView):
    def get(self, request):

        try:
            
            data = getCropsSuggestion(request.query_params.get('land'))

            return Response({'success': True,
                             'message': 'get crops suggestions',
                             'status': 200,
                             'data': data},status=status.HTTP_200_OK)
        except:
            return Response({'success': False, 'message': 'land not found!', 'status': 404},
                            status=status.HTTP_404_NOT_FOUND)

