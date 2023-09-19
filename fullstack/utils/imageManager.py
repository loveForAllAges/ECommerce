from PIL import Image
import uuid
from io import BytesIO
from django.core.files.base import ContentFile

def isImage(image_file):
    status = True
    try:
        image = Image.open(image_file)
        image.verify()
    except (IOError, SyntaxError) as error:
        status = False

    return status


def squareTheImage(image_file):
    image = Image.open(image_file)
    width, height = image.size
    size = min(width, height)

    left = (width - size) // 2
    top = (height - size) // 2
    right = (width + size) // 2
    bottom = (height + size) // 2

    cropped_image = image.crop((left, top, right, bottom))

    new_filename = f'{uuid.uuid4()}.jpg'

    temp_image_file = BytesIO()

    cropped_image.save(temp_image_file, format='JPEG')

    temp_image_file.seek(0)

    new_image = ContentFile(temp_image_file.read(), name=new_filename)

    return new_filename, new_image
