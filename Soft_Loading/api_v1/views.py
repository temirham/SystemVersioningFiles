from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.http import FileResponse
from rest_framework.pagination import PageNumberPagination

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth import authenticate, login
from rest_framework import viewsets, permissions
from Profiles.api_v1.permissions import IsManager
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

from Soft_Loading.models import *
from .serializers import *
from Soft_Site.settings import VERSION_STORAGE
from os.path import basename


class DisablePagination(PageNumberPagination):
    page_size = None


@ensure_csrf_cookie
def get_csrf_token(request):
    return Response({'csrfToken': request.csrf_token})


# For users:
class BaseAPIView(APIView):
    def get(self, request):
        dict = [
            'categories/',
            'platforms/',
            'soft/',
            'soft/<str:main_cat_id>/',
            'soft/<str:main_cat_id>/<str:sub_cat_id>/',
            'soft_data/<int:soft_id>/',
            'files/<int:file_id>/',
            'swagger/',
            'redoc/',
            'api.yaml',
            'api.json']
        return Response([request.build_absolute_uri() + item for item in dict])


class CategoriesAPIView(APIView):
    def get(self, request):
        return Response(MainCategoriesSerializer(MainCategory.objects.all(), many=True).data)


class PlatformsAPIView(APIView):
    def get(self, request):
        return Response(PlatformsSerializer(Platform.objects.all(), many=True).data)


class SoftAPIView(APIView):
    pagination_class = PageNumberPagination

    def get(self, request, **kwargs):
        # try:
            platform_id = request.GET.get('platform_id', '')
            soft_id = kwargs.get('soft_id', '')

            if soft_id == '':
                main_cat_id = kwargs.get('main_cat_id', '')
                sub_cat_id = kwargs.get('sub_cat_id', '')
                search = request.GET.get('search', '')
                base_data = {'main_cat_id': int(main_cat_id) if main_cat_id else None,
                             'sub_cat_id': int(sub_cat_id)   if main_cat_id else None,
                             'platform_id': int(platform_id) if platform_id else None,
                             'search': search}

                # Target filtering:
                soft_objects = Soft.objects.all()
                if main_cat_id != '':
                    soft_objects = soft_objects.filter(main_cat_id=main_cat_id)
                if sub_cat_id  != '':
                    soft_objects = soft_objects.filter(sub_cat_id=sub_cat_id)
                if platform_id != '':
                    soft_objects = soft_objects.filter(file__platform_id=platform_id)
                if search != '':
                    soft_objects_by_name     = soft_objects.filter(name__contains=search)
                    soft_objects_by_descr    = soft_objects.filter(description__contains=search)
                    soft_objects_by_main_cat = soft_objects.filter(sub_cat_id__main_cat_id__name__contains=search)
                    soft_objects_by_sub_cat  = soft_objects.filter(sub_cat_id__name__contains=search)

                    soft_objects = soft_objects_by_name | soft_objects_by_descr | \
                                   soft_objects_by_main_cat | soft_objects_by_sub_cat

                return Response({'query': base_data, 'data': SoftSimpleSerializer(soft_objects, many=True).data })

            else:
                soft = Soft.objects.get(soft_id=soft_id)
                return Response({'query': {'soft_id': soft_id}, 'data': SoftSerializer(soft,
                                 context={'request': request}).data})

        # except:
        #     pass


class FileAPIView(APIView):
    def get(self, request, **kwargs):
        #try:
            file_id = kwargs.get('file_id', '')
            file = File.objects.get(file_id=file_id)
            filename = Soft.objects.get(soft_id=file.soft_id.soft_id).name
            filename += '_' + file.platform_id.name.replace(' ','_') + '_' + file.architecture + \
                        '.' + basename(file.path.name).split('.')[1]

            return FileResponse(open(VERSION_STORAGE / file.path.name, 'rb'), filename=filename, as_attachment=True)

        #except FileNotFoundError:       msg = 'File not found: no in dir.'
        #except ObjectDoesNotExist:      msg = 'File not found: file or soft index error.'
        #except MultipleObjectsReturned: msg = 'File not found: file or soft duplicate error.'
        #except:                         msg = 'File not found: unknown error.'
        #finally:
            #return Response({'error': msg})


# For authorisation:
class ActiveUsersOrders(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        try:
            user = self.request.user
            username = user.username

            user = User.objects.get(id=user.id)

            user_profile = UserProfile.objects.get(user=user)
            user_profile_pk = user_profile.id

            user_profile = UserProfileSerializer(user_profile)

            orders = Orders.objects.filter(user_id=user_profile_pk)
            orders = OrdersSimpleSerializer(orders, many=True)

            return Response(orders.data)

        except:
            return Response({'error': 'something went wrong loading user'})


class BookingFilterViewSet(APIView):
    permission_classes = [IsManager]
    def get(self, request):
        query = self.request.GET.get('status')
        object_list = Booking.objects.filter(status=query)
        return Response(BookingSerializer(object_list, many=True).data)


class BookingByUserViewSet(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        query = self.request.GET.get('user')
        booking_list = Booking.objects.filter(user=query)
        service_list = booking_list[0].service
        if (booking_list is not None) and (service_list is not None):
            return Response({'booking' : BookingSerializer(booking_list[0]).data, 'service' : ServiceSerializer(service_list).data})
        else:
            return Response({'error': 'не работает'})


# For manager:
class ManagerMainCategoriesAPIView(ModelViewSet):
    pagination_class = DisablePagination
    queryset = MainCategory.objects.all()
    serializer_class = MainCategoriesSerializer


class ManagerSubCategoriesAPIView(ModelViewSet):
    pagination_class = DisablePagination
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoriesSerializer


class ManagerPlatformsAPIView(ModelViewSet):
    pagination_class = DisablePagination
    queryset = Platform.objects.all()
    serializer_class = PlatformsSerializer


class ManagerSoftAPIView(ModelViewSet):
    queryset = Soft.objects.all()
    serializer_class = SoftSerializer


class ManagerFilesAPIView(ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FilesSerializer


class ManagerSubscriptionsAPIView(ModelViewSet):
    queryset = Soft.objects.all()
    serializer_class = SoftSerializer




# class File1APIView(APIView):
#     def get(self, request, **kwargs):
#         id = kwargs.get('file_id')
#         return Response(FilesSerializer(File.objects.get(file_id = id)).data)