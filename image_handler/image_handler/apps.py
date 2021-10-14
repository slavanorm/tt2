from django.apps import AppConfig

class ImageHandlerConfig(AppConfig):
    name = 'image_handler'

    def ready(self):
        import image_handler.signals
