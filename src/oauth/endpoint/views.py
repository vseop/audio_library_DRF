from rest_framework import viewsets, parsers

class UserView(viewsets.ModelViewSet):
    """Просмотр и редактирование данных пользователя"""

    parser_classes = (parsers.MultiPartParser, )
