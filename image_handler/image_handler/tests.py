import pytest
from pytest_drf import (
    ViewSetTest,
    Returns200,
    Returns201,
    Returns204,
    UsesGetMethod,
    UsesDeleteMethod,
    UsesDetailEndpoint,
    UsesListEndpoint,
    UsesPatchMethod,
    UsesPostMethod,
    APIViewTest
)
from pytest_assert_utils import assert_model_attrs
from pytest_drf.util import pluralized, url_for
from pytest_lambda import lambda_fixture, static_fixture
from rest_framework import status
from django.core.files.base import File
from rest_framework.test import APIClient
from django.contrib.auth.models import User,Permission
from rest_framework_simplejwt.tokens import RefreshToken
from image_handler.models import ImageModel
from PIL import Image
from io import BytesIO


# todo: cleanup after tests (creates a bunch of 1*.png)


def express1(img):
    return {
        "id": img.id,
        "file":  'http://testserver' + img.file.url,
    }

express = pluralized(express1)

def get_image_file(name='test.png', ext='png', size=(50, 50),
                   color=(256, 0, 0)):
    file_obj = BytesIO()
    image = Image.new("RGB", size=size, color=color)
    image.save(file_obj, ext)
    file_obj.seek(0)
    return File(file_obj, name=name)


img_f = get_image_file()

# todo: test img_resized

#express_img = lambda x: dict(file=x.file)

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass

class TestsBase:
    # db and settings setup
    list_url = lambda_fixture(lambda: url_for("img-list"))
    detail_url = lambda_fixture(
        lambda img: url_for("img-detail", img.pk)
    )

    img = lambda_fixture(
        lambda: ImageModel.objects.create(file=img_f),
        autouse=True,
    )
    ids = lambda_fixture(
        lambda: set(
            ImageModel.objects.values_list("id", flat=True)
            )
        )

    @pytest.fixture
    def users(self):
        def create(**kwargs):
            pw = kwargs.pop('password')
            perm = kwargs.pop('permission',None)
            u = User.objects.create(**kwargs)
            u.set_password(pw)
            if perm:
                perm = Permission.objects.get(codename=perm)
                u.user_permissions.add(perm)
            u.save()

        args=[
            dict(username="admin", is_superuser=True,password='1'),
        ]

        [create(**e ) for e in args]

    @pytest.fixture
    def client(self,users):
        user = User.objects.get(id=1)
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        return client

class TestImageViewSet(
    ViewSetTest,TestsBase
):
    class TestList(
        UsesGetMethod,
        UsesListEndpoint,
        Returns200,
    ):
        def test_it(self, json, img):
            expected = [express1(img)]
            actual = json
            assert expected == actual

    class TestCreate(
        UsesPostMethod,
        UsesListEndpoint,
        Returns201,
    ):
        @pytest.fixture
        def data(self,img):
            with img.file.open() as f:
                return f

        @pytest.fixture
        def data(self,img):
            return dict(file=img.file)


        def test(self, ids, json):
            expected = ids | {json["id"]}
            actual = set(
                ImageModel.objects.values_list("id", flat=True)
            )
            assert expected == actual

        def test_returns_img(self, json):
            img = ImageModel.objects.get(pk=json["id"])

            expected = express1(img)
            actual = json
            assert expected == actual

    class TestRetrieve(
        UsesGetMethod,
        UsesDetailEndpoint,
        Returns200,
    ):
        def test(self, img, json):
            expected = express1(img)
            actual = json
            assert expected == actual

    class TestUpdate(
        UsesPatchMethod,
        UsesDetailEndpoint,
        Returns200,
    ):
        @pytest.fixture
        def data(self,img):
            return dict(file=img.file)

        def test_returns(self, img, json):
            img.refresh_from_db()

            expected = express1(img)
            actual = json
            assert expected == actual

    class TestDestroy(
        UsesDeleteMethod,
        UsesDetailEndpoint,
        Returns204,
    ):
        def test(self, ids, img):
            expected = ids - { img.id }
            actual = set(
                ImageModel.objects.values_list("id", flat=True)
            )
            assert expected == actual

class TestResized(TestsBase,
                  APIViewTest,
                  UsesPostMethod,
                  Returns200,
                  ):
    width=static_fixture(11)
    height=static_fixture(10)
    url = lambda_fixture(lambda width,height: url_for("img_resized",
                                         width=width,
                                         height=height,
                                         filename='1.jpg'))

    def test(self,response,width,height):
        img1 = Image.open(BytesIO(b''.join(response.streaming_content)))
        assert img1.width == width
        assert img1.height == height

