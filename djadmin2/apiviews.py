from django.utils.encoding import force_text

from rest_framework import fields, generics, serializers
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from . import utils
from .viewmixins import Admin2Mixin


class Admin2APISerializer(serializers.HyperlinkedModelSerializer):
    _default_view_name = 'admin2:%(app_label)s_%(model_name)s_api_detail'

    pk = fields.Field(source='pk')
    __str__ = fields.Field(source='__unicode__')


class Admin2APIMixin(Admin2Mixin):
    raise_exception = True

    def get_serializer_class(self):
        if self.serializer_class is None:
            model_class = self.get_model()

            class ModelAPISerilizer(Admin2APISerializer):
                # we need to reset this here, since we don't know anything
                # about the name of the admin instance when declaring the
                # Admin2APISerializer base class
                _default_view_name = ':'.join((
                    self.model_admin.admin.name,
                    '%(app_label)s_%(model_name)s_api_detail'))

                class Meta:
                    model = model_class

            return ModelAPISerilizer
        return super(Admin2APIMixin, self).get_serializer_class()


class IndexAPIView(Admin2APIMixin, APIView):
    apps = None
    registry = None
    version = '0'

    def get_admin_data(self, admin):
        entrypoints = []
        for version, views in admin.api.items():
            url = reverse(
                '{current_app}:{admin_name}_api_v{version}_list'.format(
                    current_app=admin.admin.name,
                    admin_name=admin.name,
                    version=version,
                ),
                request=self.request)
            entrypoints.append({
                'version': version,
                'url': url,
            })
        default_entrypoint = reverse(
            '{current_app}:{admin_name}_api_list'.format(
                current_app=admin.admin.name,
                admin_name=admin.name,
            ),
            request=self.request)
        model_options = utils.model_options(admin.model)
        verbose_name = force_text(model_options.verbose_name)
        verbose_name_plural = force_text(model_options.verbose_name_plural)
        model_data = {
            'app_label': model_options.app_label,
            'object_name': model_options.object_name,
            'verbose_name': verbose_name,
            'verbose_name_plural': verbose_name_plural,
        }
        return {
            'name': admin.name,
            'model': model_data,
            'url': default_entrypoint,
            'versions': entrypoints,
        }

    def get(self, request):
        admin_data = []
        for admin in self.registry.values():
            admin_data.append(self.get_admin_data(admin))
        index_data = {
            'version': self.version,
            'admins': admin_data,
        }
        return Response(index_data)


class ListCreateAPIView(Admin2APIMixin, generics.ListCreateAPIView):
    pass


class RetrieveUpdateDestroyAPIView(Admin2APIMixin, generics.RetrieveUpdateDestroyAPIView):
    pass
