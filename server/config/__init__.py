import logging

from utils.http import success_response, error_response
from utils.shortcuts import save_upload_file, rand_str

logger = logging.getLogger(__name__)


async def handle_upload_file(request):
    data = await request.post()
    file_obj = data['file']
    filename = file_obj.filename
    file = file_obj.file
    save_name = rand_str()

    try:
        await request.app['db'].files.insert_one({'filename': filename, 'save_name': save_name})
    except Exception as e:
        logger.exception(e)
        return error_response(request['i18n'].server_error)
    await save_upload_file(save_name, file)
    return success_response()


async def setup(app):
    app.router.add_route('POST', '/api/upload_file', handle_upload_file)
