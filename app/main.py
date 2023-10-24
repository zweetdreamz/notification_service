import traceback
import uvicorn
from fastapi import FastAPI, Depends, Response

from core import NotificationManager, get_manager
from models import CreateNotification, DefaultResponse, ListNotificationsResponse, ListRequest, ReadRequest, User

app = FastAPI()


@app.on_event('startup')
def prepare_mongo():
    notif_manager = next(get_manager())
    [notif_manager.generate() for _ in range(5)]


@app.get('/')
def read_root():
    return {'Hello': 'World'}


@app.post(
    '/api/create',
    response_model=DefaultResponse,
    status_code=201,
    response_model_exclude_unset=True
)
def create_handler(payload: CreateNotification, response: Response,
                   notif_manager: NotificationManager = Depends(get_manager)):
    try:
        res = notif_manager.create(**payload.model_dump())
        return DefaultResponse(success=res)
    except:
        response.status_code = 500
        return DefaultResponse(success=False, error=traceback.format_exc())


@app.get(
    '/api/list',
    response_model=ListNotificationsResponse | DefaultResponse,
    status_code=200,
    response_model_exclude_unset=True
)
def create_handler(response: Response, payload: ListRequest = Depends(),
                   notif_manager: NotificationManager = Depends(get_manager)):
    try:
        res = notif_manager.get_list(**payload.model_dump())
        return ListNotificationsResponse(success=True, data=res)
    except:
        response.status_code = 500
        return DefaultResponse(success=False, error=traceback.format_exc())


@app.post(
    '/api/read',
    response_model=DefaultResponse,
    status_code=200,
    response_model_exclude_unset=True
)
def read_handler(response: Response, payload: ReadRequest = Depends(),
                 notif_manager: NotificationManager = Depends(get_manager)):
    try:
        res = notif_manager.read(**payload.model_dump())
        return DefaultResponse(success=res)
    except:
        response.status_code = 500
        return DefaultResponse(success=False, error=traceback.format_exc())


@app.get(
    '/api/users',
    response_model=list[User],
    status_code=200,
)
def users_handler(response: Response,
                  notif_manager: NotificationManager = Depends(get_manager)):
    try:
        return notif_manager.get_collection()
    except:
        response.status_code = 500
        return DefaultResponse(success=False, error=traceback.format_exc())


# uvicorn.run(app, port=3000)
