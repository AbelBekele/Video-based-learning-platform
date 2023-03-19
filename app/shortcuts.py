from app import config
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

settings = config.get_settings()
templates = Jinja2Templates(directory=str(settings.templates_dir))

# will generate template response from given template & context
def render (request, template_name, context):
    contxt = context.copy()
    contxt.update({"request": request})
    return templates.TemplateResponse(template_name, contxt)