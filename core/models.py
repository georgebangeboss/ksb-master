import base64
from distutils.command.upload import upload
from fileinput import filename

from django.conf import settings
from django.db import models
from django.forms import ClearableFileInput
from django.utils import timezone
from django import template
from .garage import logo_base64_string
import base64

# from authentication.models import Client, SalesPerson, Engineer, Manager

register = template.Library()


class DailyWorkSheet(models.Model):
    client = models.CharField(max_length=200, null=True)
    client_org = models.CharField(max_length=200, null=True)
    engineer = models.CharField(max_length=200, null=True)
    manager = models.CharField(max_length=200, null=True)
    report = models.TextField()
    recommendation = models.TextField()
    action_work_required = models.TextField()
    arrival_time = models.DateTimeField(default=timezone.now)
    departure_time = models.DateTimeField(default=timezone.now)
    vehicle_reg = models.CharField(max_length=10)
    start_mileage = models.IntegerField()
    end_mileage = models.IntegerField()
    location = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    department = models.CharField(max_length=300)
    job_number = models.CharField(max_length=100, null=True)
    time_spent = models.CharField(max_length=30, null=True)
    distance_covered = models.IntegerField(null=True)
    client_signature = models.TextField()
    engineer_signature = models.TextField()
    client_sig_pic = models.BinaryField(
        null=False,
        blank=False,
    )
    engineer_sig_pic = models.BinaryField(
        null=False,
        blank=False,
    )
    work_sheet_images = models.FileField(null=True, blank=True, upload_to="work_sheet/")

    @register.filter(name="binary_to_image")
    def decode_signature(self, signature_str: str):
        return base64.decodestring(signature_str.encode())
        f = open(f"{settings.BASE_DIR}/output.png", "wb")
        f.write(img_data)
        f.close()

    def decode_client_sig(self):
        return self.decode_signature(self.client_signature)

    def decode_engineer_signature_sig(self):
        return self.decode_signature(self.engineer_signature)

    def get_distance(self):
        return self.end_mileage - self.start_mileage

    def get_logo(self):
        return logo_base64_string

    def get_worksheet_image(self):
        filename = self.work_sheet_images.path
        ext = filename.split(".")[-1]
        prefix = f"data:image/{ext};base64,"
        with open(filename, "rb") as image_file:
            encode_string_bytes = base64.b64encode(image_file.read())
            encode_string = encode_string_bytes.decode("utf8")
        return prefix + encode_string

    class Meta:
        verbose_name = "Daily Work Sheet"
        verbose_name_plural = "Daily Work Sheets"


class FieldPhoto(models.Model):
    field_image = models.FileField(null=True, blank=True, upload_to="field-photos/")
    work_sheet_id = models.ForeignKey(
        DailyWorkSheet, on_delete=models.DO_NOTHING, related_name="field_photos"
    )

    def get_worksheet_image(self):
        filename = self.work_sheet_images.path
        ext = filename.split(".")[-1]
        prefix = f"data:image/{ext};base64,"
        with open(filename, "rb") as image_file:
            encode_string_bytes = base64.b64encode(image_file.read())
            encode_string = encode_string_bytes.decode("utf8")
        return prefix + encode_string
