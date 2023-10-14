from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from django.contrib.auth.models import User
from Profiles.api_v1.serializers import UserSerializer
from GRPC.protos import minio_pb2
from GRPC.client import stub


class StorageServerError(APIException):
    status_code = 500
    default_detail = 'A problem has occurred on the storage server'
    # default_code = 'service_unavailable'


class BadRequestError(APIException):
    status_code = 400
    default_detail = 'The request could not be understood by the server due to malformed syntax or incorrect content'
    # default_code = 'service_unavailable'


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_file_versions_info(request, userId):
    print("Получение заметок пользователя номер", userId)
    userobj = User.objects.get(id=userId)
    # print(userobj) #
    username = userobj.username
    print("Пользователь:", username)
    stream = stub.GetFilesInfoList(minio_pb2.User(user=username))
    notes_list = []
    for object in stream:
        print("Заметка", object)
        note_dict = {"user": object.user, "title": object.title, "content": object.content, "date": object.date}
        notes_list.append(note_dict)
    print("Список заметок:", notes_list)
    return Response({
        'data': notes_list
    })


# Добавление заметки
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def add_file_version(request):
    print("Запрос: ", request)
    print("Тело запроса: ", request.data)
    print("Добавляем заметку: ", request.data['user'], request.data['title'], request.data['content'])
    # data = json.loads(request.data['body'])
    status = stub.AddNote(minio_pb2.NoteRequest(user=request.data['user'], title=request.data['title'],
                                                content=request.data['content']))
    if status.status:
        print("Статус операции: ", status)
        return Response({
            'status': status.status,
            'status_code': status.status_code
        })
    elif status.status_code == 400:
        raise BadRequestError
    elif status.status_code == 500:
        raise StorageServerError

# Удаление заметки
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def delete_file_version(request):
    print("Запрос: ", request)
    print("Тело запроса: ", request.data)
    # data = json.loads(request.data['body'])
    print("Удаляем заметку: ", request.data['user'], request.data['title'])
    status = stub.DeleteNote(minio_pb2.NoteTitle(user=request.data['user'], title=request.data['title']))
    if status.status:
        print("Статус операции: ", status)
        return Response({
            'status': status.status,
            'status_code': status.status_code
        })
    elif status.status_code == 400:
        raise BadRequestError
    elif status.status_code == 500:
        raise StorageServerError


@api_view(['POST'])
def getJson(request):
    print("Запрос: ", request)
    # data = json.loads(str(request.data))
    # data = json.loads(request.data['body'])
    print("Тело запроса: ", request.data)
    try:
        userobj = User.objects.get(username=request.data['username'])
    except:
        status = stub.AddUser(minio_pb2.User(user=request.data['username']))

        # print(stub)

        if status.status:
            user = User(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            print('Новый пользователь:')
            print(request.data['username'], request.data['password'])
            print("Статус операции: ", status)
            return Response({
                'status': status.status,
                'status_code': status.status_code
            })
        elif status.status_code == 400:
            raise BadRequestError
        elif status.status_code == 500:
            raise StorageServerError
    else:
    # print(userobj)
        raise BadRequestError


@api_view()
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def user(request):
    print("Запрос: ", request)
    print("Данные пользователя: ", UserSerializer(request.user).data)
    return Response({
        'data': UserSerializer(request.user).data,
    })



# # Изменение заметки
# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([JWTAuthentication])
# def edit_note(request):
#     # data = json.loads(request.data)
#     # print(data)
#     print("Запрос: ", request)
#     print("Тело запроса: ", request.data)
#     minio_date = stub.GetDate(minio_pb2.NoteTitle(user=request.data['user'], title=request.data['old_title']))
#     front_date = request.data['date']
#     print("front_date", front_date)
#     print("minio_date", minio_date.date)
#     if minio_date.date == front_date:
#         print("Редактируем заметку:", request.data['user'], request.data['old_title'])
#         status = stub.EditNote(minio_pb2.NoteRequest(user=request.data['user'], title=request.data['title'],
#                                                      content=request.data['content'],
#                                                      old_title=request.data['old_title']))
#         print("Теперь:", request.data['user'], request.data['title'], request.data['content'])
#     else:
#         print("Синхронизация, добавляем заметку:", request.data['user'], request.data['old_title'] + '(AUTO)',
#               request.data['content'])
#         status = stub.AddNote(minio_pb2.NoteRequest(user=request.data['user'],
#                                                     title=request.data['old_title'] + '(AUTO)',
#                                                     content=request.data['content']))
#     if status.status:
#         print("Статус операции: ", status)
#         return Response({
#             'status': status.status,
#             'status_code': status.status_code
#         })
#     elif status.status_code == 400:
#         raise BadRequestError
#     elif status.status_code == 500:
#         raise StorageServerError
#

