from rest_framework.response import Response
from rest_framework import status
from rest_framework.settings import api_settings
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from easy_pdf.rendering import render_to_pdf_response
from rest_framework import generics
from .utils import link_callback
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa
from easy_pdf.views import PDFTemplateResponseMixin, PDFTemplateView
from django.conf import settings
import base64
from django.http import HttpResponse
from datetime import timezone
from django.shortcuts import redirect
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email import encoders

from .models import DailyWorkSheet
from .serializers import DailyWorkSheetSerializer
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
import ssl
from django_weasyprint.utils import django_url_fetcher
from django.core.mail import EmailMessage

import tempfile
import functools
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

from django_weasyprint import WeasyTemplateResponseMixin
from django_weasyprint.views import WeasyTemplateResponse

from django.core.mail import send_mail
from django.conf import settings


class DailyWorkSheetCreateAPIView(generics.CreateAPIView):
    queryset = DailyWorkSheet.objects.all()
    serializer_class = DailyWorkSheetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            # files_list = request.FILES.getlist('work_sheet_images')
            # for item in files_list:
            # f = DailyWorkSheet.objects.create(name=request.data['name'], work_sheet_images=item)
            serializer.save()

            headers = self.get_success_headers(serializer.data)
            pk = serializer.data["id"]
            pdf_mime = generateImageMime(id=pk)
            file_name = f"work_sheet_{pk}.pdf"

            email = EmailMessage(
                "New WorkSheet",
                "A new work sheet has been created now",
                settings.EMAIL_HOST_USER,
                ["tonnymaishaogeto@gmail.com"],
                ["frankogetomitema@gmail.com"],
            )
            pdf_mime.add_header("Content-Disposition", "attachment", filename=file_name)

            email.attach(pdf_mime)
            email.send()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        return Response(
            {
                "status": "Bad request",
                "message": "Account could not be created with received data.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class DailyWorkSheetRetrieveAPIView(generics.RetrieveAPIView):
    queryset = DailyWorkSheet.objects.all()
    serializer_class = DailyWorkSheetSerializer


class DailyWorkSheetUpdateAPIView(generics.UpdateAPIView):
    queryset = DailyWorkSheet.objects.all()
    serializer_class = DailyWorkSheetSerializer


class DailyWorkSheetDeleteAPIView(generics.DestroyAPIView):
    queryset = DailyWorkSheet.objects.all()
    serializer_class = DailyWorkSheetSerializer


class DailyWorkSheetListAPIView(generics.ListAPIView):
    queryset = DailyWorkSheet.objects.all()
    serializer_class = DailyWorkSheetSerializer


def generateImageMime(id: int):
    obj = DailyWorkSheet.objects.get(pk=id)
    print(obj)
    context = {"obj": obj}
    font_config = FontConfiguration()
    htmlString = render_to_string(settings.BASE_DIR / "templates/index2.html", context)

    html = HTML(string=htmlString)

    css = CSS(
        settings.BASE_DIR / "core/static/core/mystyles.css", font_config=font_config
    )
    result = html.write_pdf(
        # settings.BASE_DIR / "files/pdf1.pdf",
        stylesheets=[css],
        optimize_size=("fonts", "images"),
        font_config=font_config,
    )

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, "rb")
    pdf_bytes = output.read()

    pdf_doc_mime = MIMEApplication(
        pdf_bytes, _subtype="pdf", _encoder=encoders.encode_base64
    )

    return pdf_doc_mime


class MyDetailView(DetailView):
    # vanilla Django DetailView
    template_name = "index2.html"
    context_object_name = "obj"
    model = DailyWorkSheet


class CustomWeasyTemplateResponse(WeasyTemplateResponse):
    # customized response class to change the default URL fetcher
    def get_url_fetcher(self):
        # disable host and certificate check
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return functools.partial(django_url_fetcher, ssl_context=context)


class PrintView(WeasyTemplateResponseMixin, MyDetailView):
    # output of MyDetailView rendered as PDF with hardcoded CSS
    pdf_stylesheets = [
        settings.BASE_DIR / "core/static/core/mystyles.css",
    ]
    # show pdf in-line (default: True, show download dialog)
    pdf_attachment = True
    # custom response class to configure url-fetcher
    response_class = CustomWeasyTemplateResponse


class DownloadView(WeasyTemplateResponseMixin, MyDetailView):
    pdf_stylesheets = [
        settings.BASE_DIR / "core/static/core/mystyles.css",
    ]
    # show pdf in-line (default: True, show download dialog)
    pdf_attachment = True
    # custom response class to configure url-fetcher
    response_class = CustomWeasyTemplateResponse
    # suggested filename (is required for attachment/download!)
    pdf_filename = "foo.pdf"


class DynamicNameView(WeasyTemplateResponseMixin, MyDetailView):
    # dynamically generate filename
    def get_pdf_filename(self):
        return "foo-{at}.pdf".format(at=timezone.now().strftime("%Y%m%d-%H%M"))
