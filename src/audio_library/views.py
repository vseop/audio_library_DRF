import os


from rest_framework import generics, viewsets, parsers, views

from . import models, serializer
from ..base.classes import MixedSerializer

from ..base.permissions import IsAuthor
from ..base.services import delete_old_file


class GenreView(generics.ListAPIView):
    """ Список жанров
    """
    queryset = models.Genre.objects.all()
    serializer_class = serializer.GenreSerializer


class LicenseView(viewsets.ModelViewSet):
    """ CRUD лицензий автора
    """
    serializer_class = serializer.LicenseSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return models.License.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AlbumView(viewsets.ModelViewSet):
    """ CRUD альбомов автора
    """
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = serializer.AlbumSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return models.Album.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        instance.delete()


class PublicAlbumView(generics.ListAPIView):
    """ Список публичных альбомов автора
    """
    serializer_class = serializer.AlbumSerializer

    def get_queryset(self):
        return models.Album.objects.filter(user__id=self.kwargs.get('pk'), private=False)

class TrackView(MixedSerializer, viewsets.ModelViewSet):
    """ CRUD треков
    """
    parser_classes = (parsers.MultiPartParser,)
    permission_classes = [IsAuthor]
    serializer_class = serializer.CreateAuthorTrackSerializer
    serializer_classes_by_action = {
        'list': serializer.AuthorTrackSerializer
    }

    def get_queryset(self):
        return models.Track.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        delete_old_file(instance.file.path)
        instance.delete()


