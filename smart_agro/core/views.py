from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import SoilData
from .serializers import SoilDataSerializer

class SoilDataView(APIView):
    def get(self, request):
        try:
            soil_data_objects = SoilData.objects.filter(land=request.query_params.get('land'))
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
