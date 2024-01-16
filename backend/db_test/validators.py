from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions


def validate_file_size(value):
    filesize= value.size
    if filesize > 4*1024*1024:
        raise ValidationError("The maximum file size that can be uploaded is 4MB")
    # picture = value.cleaned_data.get("picture")
    # w, h = get_image_dimensions(picture)
    # if not w < 1 or w > 6:
    #     raise ValidationError("Wrong image size")
    # if not h < 1 or h > 6:
    #     raise ValidationError("Wrong image size")
    return value
