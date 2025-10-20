from rest_framework import generics, permissions
from .models import Show
from .serializers import ShowSerializer

# GET /api/shows/ - список усіх вистав/ств. нову виставу для адміна
class ShowListView(generics.ListCreateAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]  # створювати може лише адмін
        return [permissions.AllowAny()]  # переглядати можуть всі

# GET /api/shows/{id}/ - деталі конкретної вистави/оновити/видалити
class ShowDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
