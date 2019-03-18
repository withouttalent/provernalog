from django.shortcuts import HttpResponse
from async_parser.models import ParserTask, TaskFile
from async_parser.tasks import add_parcel
from async_parser.management.commands.scraping import Command
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import os


def retry_file(request, file_id):
    celery_id = request.GET.get('celery_id')
    if not celery_id:
        return HttpResponse(status=400)
    try:
        file = TaskFile.objects.get(pk=file_id, celery_id=celery_id)
    except TaskFile.DoesNotExist:
        return HttpResponse(status='404', content="File doesn't exist")
    file.parsed_parcels = None
    file.parcels = None
    file.errors = None
    file.is_parsed = False
    file.save()
    celery = add_parcel.delay(file=file.path, task_file_id=file.id,
                              region=file.task.city.region,
                              group_type=file.task.group_type, date_relevance=file.task.date_relevance)
    return HttpResponse(status=200, content_type='application/json')


@csrf_exempt
def create_task(request):

    if request.method == 'POST':
        data = {}
        for key, value in request.POST.items():
            data[key] = value if value else None
        if list(data.keys()) == ['file', 'group_type', 'region', 'date_relevance', 'secret_key']:
            if data['secret_key'] == settings.LOGGING_SECRET_KEY:
                command = Command()
                data['file'] = os.path.join('/mnt/ftp/ziparchive', data['file'])
                command.arguments['path'] = data['file']
                command.arguments['region'] = data['region']
                command.arguments['date_relevance'] = data['date_relevance']
                command.arguments['group_type'] = data['group_type']
                command.path_preparation()
                task = command.task_register()
                command.create_task()
                task_json = dict(
                    id=task.id,
                    path=task.path,
                    city_name=task.city.name,
                    city_region=task.city.region,
                    group_type=task.group_type,
                    date_created=task.date_created.strftime('%Y-%m-%d %H:%M:%S') if task.date_created else None
                    )
                task_json = json.dumps(task_json)
                return HttpResponse(status=201, content=task_json, content_type='application/json')
    return HttpResponse(status=400, content_type='application/json')
