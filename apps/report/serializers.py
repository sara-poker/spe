from rest_framework.serializers import BaseSerializer
from rest_framework import serializers

from apps.test.models import Isp

PROVINCES_FA = {
    "Alborz": "البرز",
    "Ardabil": "اردبیل",
    "Aazerbaijan-East": "آذربایجان شرقی",
    "Bushehr": "بوشهر",
    "Chahaar-Mahaal-Bakhtiaari": "چهارمحال و بختیاری",
    "Fars": "فارس",
    "Gilaan": "گیلان",
    "Golestaan": "گلستان",
    "Hamadaan": "همدان",
    "Hormozgaan": "هرمزگان",
    "Ilaam": "ایلام",
    "Isfahaan": "اصفهان",
    "Kermaan": "کرمان",
    "Kermanshaah": "کرمانشاه",
    "Khoraasaan-North": "خراسان شمالی",
    "Khoraasaan-Razavi": "خراسان رضوی",
    "Khoraasaan-South": "خراسان جنوبی",
    "Khuzestaan": "خوزستان",
    "Kohgiluyeh-Boyer-Ahmad": "کهگیلوی و بویراحمد",
    "Kurdistaan": "کردستان",
    "Lorestaan": "لرستان",
    "Markazi": "مرکزی",
    "Maazandaraan": "مازندران",
    "Qazvin": "قزوین",
    "Qom": "قم",
    "Semnaan": "سمنان",
    "Sistaan-Baluchestaan": "سیستان و بلوچستان",
    "Tehran": "تهران",
    "Yazd": "یزد",
    "Zanjaan": "زنجان",

}


class GetAllIspAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = Isp
        fields = ['id', 'name', 'url', 'isp', 'org', 'as_number', 'asname']
