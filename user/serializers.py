from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema

from rest_framework import serializers

User = get_user_model()

class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # serializer 의 validate 오버라이딩
    # ✔ 기본적으로 ModelSerializer는 자동으로 필드 검증을 수행하지만,
    # ✔ Django의 비밀번호 검증(validate_password())은 자동으로 실행되지 않음.
    # ✔ 따라서 추가적으로 직접 validate_password()를 호출해야 비밀번호 강도 검증이 가능하다.
    def validate(self, data):
        user = User(**data) # 유저 모델의 인스턴스 제작
        # validate_password()는 user에 User 객체를 기대함.
        # ✔ **data는 단순한 딕셔너리(예: {'email': 'test@example.com', 'password': 'pass1234'})
        # ✔ 하지만 validate_password()는 user 매개변수에 User 객체를 요구하므로, **data를 바로 넣으면 오류 발생

        errors = dict()
        try :
            # Django 기본 패스워드 검증 함수 (settings.py에 설정된 기본 정책 사용)
            validate_password(password=data['password'], user = user)
        except ValidationError as e:
            errors['password'] = list(e.messages) # 패스워드 검증 에러 메시지를 리스트로 저장

        if errors :
            raise serializers.ValidationError(errors)
        return super().validate(data) # 검증이 끝나면 기본 검증 을 사용해 모든 검증 진행


    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save() # instance 가 있으면 create 없으면 update 호출

        return user

