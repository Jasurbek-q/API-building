from django.shortcuts import render  # Hozir bu faylda ishlatilmayapti, odatda web sahifa chiqarish uchun kerak bo‘ladi
from rest_framework import generics  # Django uchun tayyor "tayyor funksiyalar to‘plami"
# Masalan: ro‘yxat chiqarish, qo‘shish, bitta narsani olish kabi ishlarni o‘zi qilib beradi
from rest_framework import permissions  # Kim nima qila olishini boshqaradi (hamma ko‘radimi, faqat loginmi va h.k.)
from rest_framework import filters  # Qidirish va saralash (filter, search, ordering) qilish uchun
from django_filters.rest_framework import DjangoFilterBackend  # Aniq field bo‘yicha filter qilish uchun
from rest_framework.permissions import SAFE_METHODS  # Xavfsiz so‘rovlar (faqat ko‘rish uchun: GET, HEAD, OPTIONS)
from .models import Vacancy  # Bazadagi “Vakansiya” jadvali (ish e’lonlari saqlanadigan joy)
from .serializers import VacancySerializer  # Ma’lumotni JSON ko‘rinishga o‘tkazib beradi (frontend tushunishi uchun)


class VacancyCreateAPIView(generics.ListCreateAPIView):

    queryset = Vacancy.objects.all().order_by('-created_ad')
    #  Bazadan hamma vakansiyalarni olib keladi
    #  Eng yangilari tepada chiqadi

    serializer_class = VacancySerializer
    #  Bazadagi ma’lumotni frontend tushunadigan ko‘rinishga o‘giradi

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    #  Hamma vakansiyalarni ko‘ra oladi
    #  Lekin yangi vakansiya qo‘shish uchun login bo‘lish shart

    filter_backends = (
        filters.SearchFilter,        # Qidirish (masalan: Google deb yozsa Google chiqadi)
        DjangoFilterBackend,         # Aniq filter (company=Google kabi)
        filters.OrderingFilter       # Tartiblash (maosh katta-kichik)
    )

    filterset_fields = ('company',)
    #  Faqat kompaniya bo‘yicha aniq filter qilish mumkin

    search_fields = ('title', 'company')
    #  Foydalanuvchi yozgan so‘z bo‘yicha qidiradi

    ordering_fields = ('created_ad', 'salary')
    #  Qaysi ustun bo‘yicha tartiblash mumkinligini belgilaydi

    def perform_create(self, serializer):
        #  Yangi vakansiya yaratilayotganda avtomatik ishlaydi

        serializer.save(user=self.request.user)
        #  Vakansiyani kim qo‘shgan bo‘lsa, o‘sha odam egasi qilib yozib qo‘yadi

class VacancyDetailAPIView(generics.RetrieveAPIView):

    queryset = Vacancy.objects.all()
    #  Bazadan vakansiyalarni olib kelish manbasi

    serializer_class = VacancySerializer
    #  Vakansiyani chiroyli JSON ko‘rinishga o‘tkazadi

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #  Hamma ko‘ra oladi, lekin o‘zgartirish uchun login kerak (bu viewda esa faqat ko‘rish bor)

    def get_object(self):
        #  Bitta vakansiyani topib olish jarayoni
        obj = super().get_object()
        #  URLdagi ID bo‘yicha vakansiyani bazadan olib keladi

        #  Agar kimdir o‘zgartirish qilmoqchi bo‘lsa tekshiradi
        if self.request.method not in SAFE_METHODS:
            #  Agar vakansiya egasi boshqa odam bo‘lsa
            if obj.user != self.request.user:
                self.permission_denied(
                    self.request,
                    message="Siz bu vakansiyani qo‘shmagansiz, o‘zgartira olmaysiz!"
                )
                #  Ruxsat yo‘q deb xatolik chiqaradi (403 Forbidden)
        return obj
        #  Agar hammasi to‘g‘ri bo‘lsa, vakansiyani foydalanuvchiga qaytaradi