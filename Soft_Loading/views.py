from django.shortcuts import render, redirect
from Soft_Loading.models import *
from django.http import HttpResponseServerError, HttpResponseNotFound, FileResponse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from Soft_Site.settings import VERSION_STORAGE
from os.path import basename

# <!--    {% paginate 12 soft_list %}--> <!--{% show_more %}-->
import psycopg2
conn = psycopg2.connect(dbname='Soft_Site_V1', user='postgres',
                        password='Root_777', host='127.0.0.1', port='5432')
conn.set_isolation_level(0)


# Technical:
def get_categ_dict():
    categ_dict = {}
    sub_cats_list = []

    for main_cat_in in MainCategory.objects.all():
        for sub_cat_in in SubCategory.objects.filter(main_cat_id=main_cat_in.main_cat_id):
            sub_cats_list.append(sub_cat_in.name)

        sub_cats_list.sort(key=str.lower)
        try:
            sub_cats_list.append(sub_cats_list.pop(sub_cats_list.index('другое')))
        except:
            pass
        categ_dict[main_cat_in.name] = sub_cats_list.copy()
        sub_cats_list.clear()

    return categ_dict


def get_soft_data(soft, is_soft_view=False):
    data = {
        'id': soft.soft_id, 'name': soft.name,
        'image': soft.image,
        'status': 'Бесплатно' if not soft.is_primary else 'Подписка',
    }
    if not is_soft_view:
        data.update({'main_cat': soft.main_cat_id.name,           # ' ' space is important
                     'sub_cat':  soft.sub_cat_id.name if soft.sub_cat_id != None else ' ',
                     'description': soft.description})

    return data


# if you use some get parameter to init redirect or create filter, and you don't want to drop other post parameters,
# that function will be helpful, it even hides redirection parameter:
def save_params_while_redir_by_get_trigger(request, trigger_parameter_name, trigger_old_value,
                                           redirect_to, redirect_kwargs):
    new_trigger_value = request.GET.get(trigger_parameter_name, '')

    # checking trigger:
    if new_trigger_value != trigger_old_value and new_trigger_value != '':  # '' - if there isnt trigger at all

        # deleting trigger value from get:
        str = ''
        if len(request.GET) > 1:
            str += '?'
            for name, value in request.GET.items():
                if name != trigger_parameter_name: str += name + '=' + value + '&'
            str = str[:len(str)-1]

        # redirecting with trigger parameter value:
        kwargs = {trigger_parameter_name: new_trigger_value}
        kwargs.update(redirect_kwargs)
        redirect_response = redirect(redirect_to, permanent=True, **kwargs)

        # adding other parameters (but not trigger):
        redirect_response['Location'] += str
        return redirect_response


def filter(request, language, main_cat='', sub_cat=''):

    kwargs = {}
    if main_cat != '': kwargs.update({'main_cat': main_cat})
    if sub_cat !='':   kwargs.update({'sub_cat': sub_cat})

    # processing language redirect:
    redirect_response = save_params_while_redir_by_get_trigger(request, 'language', language,
                                                               'soft_loading:sl_filter', kwargs)
    if redirect_response != None:
        return redirect_response

    platform = request.GET.get('plantf', '')
    #page = request.GET.get('page', '')

    #processing deleting:
    soft_id = request.POST.get('delete', '')
    if soft_id != '':
        with conn.cursor() as curs:
                # relations are deleted by cascade
                curs.execute(f'DELETE FROM "Soft" WHERE "SoftID" = {soft_id}')


    # displaying left nav:
    categ_dict = get_categ_dict()

    # getting soft:
    soft_objects = Soft.objects.all()

    # search filtering (should be first or filtration logic would be damaged):
    search = request.GET.get('search', 'none')
    if search != 'none':
        soft_objects_by_name     = soft_objects.filter(name__contains=search)
        soft_objects_by_descr    = soft_objects.filter(description__contains=search)
        soft_objects_by_main_cat = soft_objects.filter(sub_cat_id__main_cat_id__name__contains=search)
        soft_objects_by_sub_cat  = soft_objects.filter(sub_cat_id__name__contains=search)

        # type is saved:
        soft_objects = soft_objects_by_name | soft_objects_by_descr | \
                       soft_objects_by_main_cat | soft_objects_by_sub_cat

    # main category filtering:
    if main_cat != '':
        soft_objects = soft_objects.filter(main_cat_id__name=main_cat.replace('_', ' '))

    # sub category filtering:
    if sub_cat != '':
        soft_objects = soft_objects.filter(sub_cat_id__name=sub_cat.replace('_', ' '))

    # platform filtering:
    if platform != '':
        soft_objects = soft_objects.filter(files__platform_id__name=platform.title())

    # ammount filtering:
    try:
        soft_objects = soft_objects[:int(request.POST.get('ammount', 'none'))]
    except:
        pass

    # displaying soft:
    soft_list = []
    for soft in soft_objects:
        soft_list.append(get_soft_data(soft))

    #soft_list = [{'id': 97, 'main_cat':1, 'sub_cat':2, 'name': 'Microsoft Word', 'image': 'https://avatars.mds.yandex.net/i?id=64dc321a9e9afbc842f2d3b80960916745574d03-8341266-images-thumbs&n=13&exp=1', 'descr':'Programm from Microsoft...' },
    #            {'id': 97, 'main_cat':1, 'sub_cat':2,'name': 'Microsoft Exel', 'image': 'https://avatars.mds.yandex.net/i?id=132029d4337cbe2281cd2b83d80a098a72518833-4119687-images-thumbs&n=13&exp=1', 'descr': 'Programm from Microsoft...'},
    #            {'id': 97, 'main_cat':1, 'sub_cat':2, 'name': 'Microsoft Acces', 'image': 'https://avatars.mds.yandex.net/i?id=156f20350b03be4ad8f21a7ee808350822c1b4b7-9211418-images-thumbs&n=13&exp=1', 'descr': 'Programm from Microsoft...'},
    #            {'id': 97, 'main_cat':1, 'sub_cat':2,'name': 'Microsoft Office', 'image': 'https://avatars.mds.yandex.net/i?id=37a5a95b027115de7d0e77cd6094b0f757280b4d-7755612-images-thumbs&n=13&exp=1', 'descr': 'Office programms pac...'}
    #            ]

    return render(request, 'Soft_Loading/index.html', {'language': language,
                                                       'categories_dict': categ_dict,
                                                       'main_cat': main_cat,
                                                       'sub_cat': sub_cat,
                                                       'platform': platform,
                                                       'soft_list': soft_list})


def soft_object(request, language, main_cat, sub_cat, soft_id):
    # try:
        # Displaying left nav:
        categ_dict = get_categ_dict()

        # Getting soft data:
        soft = Soft.objects.get(soft_id=soft_id)
        files = File.objects.filter(soft_id=soft_id)

        platforms = Platform.objects.none()
        for file in files:
            platforms = platforms.union(Platform.objects.filter(platform_id=file.file_id))

        soft_data = get_soft_data(soft, is_soft_view=True)
        soft_data.update({
            'platforms': platforms,
            'downloads': None, 'favorites': None
        })

        # Getting files data:
        platform = request.GET.get('platform', '')
        if platform != '':
            files.filter(platform_id__name=platform)

        files_data = []
        for file in files:
            files_data.append({'id': file.file_id,
                               'architecture': file.architecture,
                               'size': file.size,
                               'version': file.version,
                               'compatibility': file.compatibility})
        # if len(files_data) == 0: files_data.append({'id': 1})

        # Getting target file with late version for selected/most popular platform
        platform = platform or Platform.objects.order_by('platform_id')[0].name
        try:
            target_file = files.filter(platform_id__name=platform).order_by('-version')[0]
            # print(files.filter(platform_id__name=platform).order_by('-version'))
        except IndexError: target_file = ''

        return render(request, 'Soft_Loading/soft.html', {'language': language,
                                                          'categories_dict': categ_dict,
                                                          'main_cat': main_cat,
                                                          'sub_cat': sub_cat,
                                                          'platform': platform,
                                                          'soft': soft_data,
                                                          'files': files_data,
                                                          'target_file': target_file})
    # Errors pocessing:
    # except ObjectDoesNotExist:      return HttpResponseServerError('<h1>The software is not found.</h1>')
    # except MultipleObjectsReturned: return HttpResponseServerError('<h1>The software is duplicated.</h1>')
    # except:
    #     return HttpResponseServerError('<h1>Soft fetching error has occurred.</h1>')


def download(request, file_id):
    # try:
        file = File.objects.get(file_id=file_id)
        filename = Soft.objects.get(soft_id=file.soft_id.soft_id).name.replace(' ','_')
        filename += '_' + file.platform_id.name + '_' + file.architecture + \
                    '.' + file.path.name.split('.')[1]
        return FileResponse(open(VERSION_STORAGE / file.path.name, 'rb'), filename=filename, as_attachment=True)
    # except FileNotFoundError:
    #     return HttpResponseNotFound('Files are not found')
    #
    # except ObjectDoesNotExist:      return HttpResponseNotFound('Version is not found')
    # except MultipleObjectsReturned: return HttpResponseServerError('<h1>Version is duplicated.</h1>')
    # except:
    #     return HttpResponseServerError('<h1>Downloading error has occurred.</h1>')


def login(request, language):
    return render(request, 'Soft_Loading/login.html', {'language': language})


def register(request, language):
    return render(request, 'Soft_Loading/register.html', {'language': language})


# technical redirect if language is not set:
def lang_redi(request):
    return redirect('soft_loading:sl_filter', permanent=False, language='ru')


