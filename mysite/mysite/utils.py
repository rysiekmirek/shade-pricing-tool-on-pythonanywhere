from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import os
from django.conf import settings
from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, encoding="UTF-8", link_callback=fetch_resources)

    if pdf.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return HttpResponse(result.getvalue(), content_type='application/pdf')


def fetch_resources(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))

    return path


