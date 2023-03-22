from app import config
from cassandra.cqlengine.query import DoesNotExist, MultipleObjectsReturned
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException


settings = config.get_settings()
templates = Jinja2Templates(directory=str(settings.templates_dir))


def is_htmx(request:Request):
    return request.headers.get("hx-request") == 'true'

# will generate template response from given template & context
def render (request, template_name, context={}, status_code:int=200, cookies:dict={}):
    contxt = context.copy()
    contxt.update({"request": request})
    # Retruning back the template
    t = templates.get_template(template_name)
    html_str = t.render(contxt)
    response = HTMLResponse(html_str, status_code=status_code)
    if len(cookies.keys()) > 0:
        for k, v in cookies.items():
            response.set_cookie(key=k, value=v, httponly=True)
    # cookie deletion
    #for key in request.cookies.keys():
    #    response.delete_cookie(key)        
    return response
    #return templates.TemplateResponse(template_name, contxt, status_code=status_code)

def redirect(path, cookies:dict={}, remove_session=False):
    response = RedirectResponse(path, status_code=302)
    for k, v in cookies.items():
        response.set_cookie(key=k, value=v, httponly=True)
    if remove_session is True:
        response.set_cookie(key="session_ended", value="1", httponly=True)
        response.delete_cookie("session_id")
    return response

def find_object(classname, **kwargs):
    obj = None
    try:
        obj = classname.objects.get(**kwargs)
    except DoesNotExist:
        raise StarletteHTTPException(status_code=404)
    except MultipleObjectsReturned:
        raise StarletteHTTPException(status_code=400)
    except:
        raise StarletteHTTPException(status_code=500)
    return obj
