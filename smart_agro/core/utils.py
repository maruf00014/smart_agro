from .models import SoilData, Land, CropsData
from .serializers import FarmerSerializer

class SubtractionMatrix:
  def __init__(self, crops_data, N_index, P_index, K_index, S_index, pH_index, moisture_index, average_index):
    self.crops_data = crops_data
    self.N_index = N_index
    self.P_index = P_index
    self.K_index = K_index
    self.S_index = S_index
    self.pH_index = pH_index
    self.moisture_index = moisture_index
    self.average_index = average_index


def getCropsSuggestion(land):

  soil_data_objects = SoilData.objects.filter(land=land).order_by('-time')

  average_N = 0
  average_P = 0
  average_K = 0
  average_S = 0
  average_pH = 0.0
  average_moisture = 0
  
  soil_data_objects_length = len(list(soil_data_objects))

  if(soil_data_objects_length > 0):
    for soil_data in soil_data_objects:
        average_N += soil_data.N
        average_P += soil_data.P
        average_K += soil_data.K
        average_S += soil_data.S
        average_pH += soil_data.pH
        average_moisture += soil_data.moisture


    average_N = int(average_N / soil_data_objects_length)
    average_P = int(average_P / soil_data_objects_length)
    average_K = int(average_K / soil_data_objects_length)
    average_S = int(average_S / soil_data_objects_length)
    average_pH /= soil_data_objects_length
    average_moisture = int(average_moisture / soil_data_objects_length)

  crops_data_objects = list(CropsData.objects.all())
  candidate_crops = list()

  for crops_data in crops_data_objects:
      if average_N <= crops_data.t_N and \
              average_P <= crops_data.t_P and \
              average_K <= crops_data.t_K and \
              average_S <= crops_data.t_S and \
              average_pH <= crops_data.t_pH and \
              average_moisture <= crops_data.t_moisture:
        candidate_crops.append(crops_data)

  candidate_subtraction_matrix_list = list()

  for crops_data in candidate_crops:
      candidate_subtraction_matrix_list.append(
          SubtractionMatrix(crops_data=crops_data,
                            N_index=average_N - crops_data.N,
                            P_index=average_P - crops_data.P,
                            K_index=average_K - crops_data.K,
                            S_index=average_S - crops_data.S,
                            pH_index=average_pH - crops_data.pH,
                            moisture_index=average_moisture - crops_data.moisture,
                            average_index= None))

  adjustment_needed_crops_matrix = list()
  no_adjustment_needed_crops_matrix = list()

  for candidate_subtraction_matrix in candidate_subtraction_matrix_list:
      if candidate_subtraction_matrix.N_index < 0 or \
              candidate_subtraction_matrix.P_index < 0 or \
              candidate_subtraction_matrix.K_index < 0 or \
              candidate_subtraction_matrix.S_index < 0 or \
              candidate_subtraction_matrix.pH_index < 0 or \
              candidate_subtraction_matrix.moisture_index < 0:
          adjustment_needed_crops_matrix.append(candidate_subtraction_matrix)

      else:
          no_adjustment_needed_crops_matrix.append(candidate_subtraction_matrix)

  no_adjustment_needed_crops_suggestions = list()

  for crops in no_adjustment_needed_crops_matrix:
      average_index = (crops.N_index +
                      crops.P_index +
                      crops.K_index +
                      crops.S_index +
                      crops.pH_index +
                      crops.moisture_index) / 6
      crops.average_index = average_index
      no_adjustment_needed_crops_suggestions.append(crops)


  no_adjustment_needed_crops_suggestions.sort(key= lambda c: c.average_index)

  adjustment_needed_crops_suggestions = list()

  for crops in adjustment_needed_crops_matrix:
      average_index = (abs(crops.N_index) +
                      abs(crops.P_index) +
                      abs(crops.K_index) +
                      abs(crops.S_index) +
                      abs(crops.pH_index) +
                      abs(crops.moisture_index)) / 6
      crops.average_index = average_index
      adjustment_needed_crops_suggestions.append(crops)

  adjustment_needed_crops_suggestions.sort(key=lambda c: c.average_index)


  crops_suggestions = no_adjustment_needed_crops_suggestions + adjustment_needed_crops_suggestions

  print(" %s  %s %s  %s %s  %s" % (average_N, average_P,average_K,average_S,average_pH,average_moisture))

  for crop in crops_suggestions:
      print(crop.crops_data.crops_name)

  land = Land.objects.get(pk=land)

  crops_suggestions_response = list()

  for crop in crops_suggestions:
      crops_suggestions_response.append({
      'id': crop.crops_data.id,
      'crops_name':  crop.crops_data.crops_name,
      'average_index':  round(crop.average_index, 3),
      'N': crop.crops_data.N,
      't_N': crop.crops_data.t_N,
      'P': crop.crops_data.P,
      't_P': crop.crops_data.t_P,
      'K': crop.crops_data.K,
      't_K': crop.crops_data.t_K,
      'S': crop.crops_data.S,
      't_S': crop.crops_data.t_S,
      'pH': crop.crops_data.pH,
      't_pH': crop.crops_data.t_pH,
      'moisture': crop.crops_data.moisture,
      't_moisture': crop.crops_data.t_moisture,
      # 'N_index': crop.N_index,
      # 'P_index': crop.P_index,
      # 'K_index': crop.K_index,
      # 'S_index': crop.S_index,
      # 'pH_index': crop.pH_index,
      # 'moisture_index': crop.moisture_index,

      })

  farmer_serializer = FarmerSerializer(land.farmer.all(),many=True)
  data = {
      'id': land.id,
      'name': land.name,
      'farmer': farmer_serializer.data,
      'area': land.area,
      'address': land.address,
      'ave_N': average_N,
      'ave_P': average_P,
      'ave_K': average_K,
      'ave_S': average_S,
      'ave_pH': average_pH,
      'ave_moisture': average_moisture,
      'crops_suggestion': crops_suggestions_response

  }

  return data





