from rest_framework import serializers
from .models import Vacancy

class VacancySerializer(serializers.ModelSerializer):
  #  'owner' maydonini faqat oqish uchun qilamiz (read only)
  #   chunki kim elo yuboryotganini API dan emas. Sorov yuborgan tokendan bilamiz
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Vacancy
        fields = '__all__'


