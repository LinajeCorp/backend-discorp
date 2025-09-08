from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo User venezolano con campos personalizados
    """
    documento_completo = serializers.ReadOnlyField(
        help_text="Documento con formato completo (ej: V-12345678)"
    )
    password = serializers.CharField(
        write_only=True,
        help_text="Contraseña del usuario (mínimo 8 caracteres)"
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username', 
            'email',
            'first_name',
            'last_name',
            'direccion',
            'tipo_documento',
            'documento',
            'documento_completo',
            'password',
            'is_active',
            'date_joined'
        ]
        extra_kwargs = {
            'username': {
                'help_text': 'Nombre de usuario único (requerido)'
            },
            'email': {
                'help_text': 'Correo electrónico válido'
            },
            'first_name': {
                'help_text': 'Nombre del usuario'
            },
            'last_name': {
                'help_text': 'Apellido del usuario'
            },
            'direccion': {
                'help_text': 'Dirección completa del usuario en Venezuela'
            },
            'tipo_documento': {
                'help_text': 'Tipo de documento: V (Cédula), E (Extranjero), P (Pasaporte), J (RIF Jurídico), G (RIF Gubernamental)'
            },
            'documento': {
                'help_text': 'Número de documento sin espacios ni guiones'
            },
            'is_active': {
                'read_only': True,
                'help_text': 'Indica si el usuario está activo'
            },
            'date_joined': {
                'read_only': True,
                'help_text': 'Fecha de registro del usuario'
            }
        }

    def create(self, validated_data):
        """Crear usuario con contraseña encriptada"""
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user

    def update(self, instance, validated_data):
        """Actualizar usuario, manejando contraseña por separado"""
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer específico para registro de usuarios venezolanos
    """
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text="Contraseña mínimo 8 caracteres"
    )
    password_confirm = serializers.CharField(
        write_only=True,
        help_text="Confirmación de contraseña"
    )
    documento_completo = serializers.ReadOnlyField(
        help_text="Documento formateado automáticamente"
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password_confirm',
            'first_name',
            'last_name',
            'direccion',
            'tipo_documento',
            'documento',
            'documento_completo'
        ]
        extra_kwargs = {
            'username': {
                'help_text': 'Nombre de usuario único'
            },
            'email': {
                'help_text': 'Correo electrónico válido'
            },
            'first_name': {
                'help_text': 'Nombre (requerido)'
            },
            'last_name': {
                'help_text': 'Apellido (requerido)'
            },
            'direccion': {
                'help_text': 'Dirección completa en Venezuela'
            },
            'tipo_documento': {
                'help_text': 'V=Cédula, E=Extranjero, P=Pasaporte, J=RIF Jurídico, G=RIF Gubernamental'
            },
            'documento': {
                'help_text': 'Número de documento (solo números)'
            }
        }

    def validate(self, attrs):
        """Validar que las contraseñas coincidan"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'Las contraseñas no coinciden'
            })
        return attrs

    def create(self, validated_data):
        """Crear usuario eliminando password_confirm"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer personalizado para JWT que incluye información del usuario venezolano
    """
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Agregar información adicional del usuario al token
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'documento_completo': self.user.documento_completo,
            'is_staff': self.user.is_staff,
        }
        
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Agregar claims personalizados al token
        token['username'] = user.username
        token['email'] = user.email
        if user.documento_completo:
            token['documento'] = user.documento_completo
        
        return token


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer para perfil de usuario (solo lectura con información completa)
    """
    documento_completo = serializers.ReadOnlyField(
        help_text="Documento con formato V-12345678"
    )
    full_name = serializers.SerializerMethodField(
        help_text="Nombre completo del usuario"
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'direccion',
            'tipo_documento',
            'documento',
            'documento_completo',
            'is_active',
            'is_staff',
            'date_joined',
            'last_login'
        ]
        read_only_fields = ['id', 'username', 'is_active', 'is_staff', 'date_joined', 'last_login']

    def get_full_name(self, obj):
        """Retorna el nombre completo del usuario"""
        return f"{obj.first_name} {obj.last_name}".strip()
