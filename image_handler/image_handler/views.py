from image_handler.models import ImageModel
from image_handler import settings
from image_handler.serializers import (
    ImageSerializer,
)
import os
try:
    from PIL import Image
except ModuleNotFoundError:
    import Image

from django.http import FileResponse
from rest_framework import permissions, viewsets


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    queryset = ImageModel.objects.all()
    if not settings.DEBUG:
        permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def resized(request, width: int, height: int, filename: str):
        pk = int(os.path.splitext(os.path.basename(filename))[0])
        img = ImageModel.objects.get(pk=pk)

        fp = os.path.join(
            settings.MEDIA_ROOT,
            "resized",
            "%s_%s_%s" % (width, height, img.file.name),
        )
        if not os.path.exists(fp):
            result = Image.open(img.file)
            # can use thumbnail to keep aspect ratio
            result = result.resize(
                [width, height],
                Image.ANTIALIAS,
            )
            result.save(fp)

        r = FileResponse(open(fp, "rb"))
        return r
