from rest_framework.serializers import ModelSerializer,Serializer,CharField,ValidationError
from django.contrib.auth import authenticate

from django.contrib.auth import get_user_model

User  = get_user_model()

class User_serializers(ModelSerializer):

    def create(self,validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data) #this creates a object of the give user

        if password is not None:
            instance.set_password(password) 
        instance.save()
        return instance
        
    
    class Meta:
        model = User
        extra_kwargs = {"password":{'write_only':True}}
        fields = ['username','password','first_name']




class Userlogin_serializer(Serializer):
    username = CharField()
    password = CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise ValidationError('Invalid credentials')
        else:
            raise ValidationError('Username and password are required')

        data['user'] = user
        return data