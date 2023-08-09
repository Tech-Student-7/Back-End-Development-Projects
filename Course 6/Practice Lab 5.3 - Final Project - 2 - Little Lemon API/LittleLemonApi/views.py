from rest_framework import generics
from .serializers import MenuItemSerializer,CartSerializer,UserSerializer,OrdersSerializer
from .models import MenuItem,Cart,Order,OrderItem
from rest_framework.permissions import IsAdminUser,IsAuthenticated,AllowAny
from django.contrib.auth.models import User,Group
from decimal import Decimal
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

# Create your views here.
class MenuItemView(generics.ListCreateAPIView):
    queryset=MenuItem.objects.all()
    serializer_class=MenuItemSerializer
    ordering_fields=['price']
    search_fields=['title']
    throttle_classes=[AnonRateThrottle,UserRateThrottle]
    
    def get_permissions(self):
        if self.request.method=='POST':
            return [IsAdminUser()]
        return[AllowAny()]
    
class SingleItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset=MenuItem.objects.all()
    serializer_class=MenuItemSerializer
    throttle_classes=[AnonRateThrottle,UserRateThrottle]
    
    def get_permissions(self):
        if self.request.method=='POST' or self.request.method=='DELETE' or self.request.method=='PATCH' or self.request.method=='PUT':
            return [IsAdminUser()]
        return[AllowAny()]
    
class UsersView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        manager_group = Group.objects.get(name='manager')
        queryset = User.objects.filter(groups=manager_group)
        return queryset

    def perform_create(self, serializer):
        manager_group = Group.objects.get(name='manager')
        user = serializer.save()
        user.groups.add(manager_group)


class SingleUserView(generics.RetrieveDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        manager_group = Group.objects.get(name='manager')
        queryset = User.objects.filter(groups=manager_group)
        return queryset
    
class crewView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        delivery_group = Group.objects.get(name='delivery crew')
        queryset = User.objects.filter(groups=delivery_group)
        return queryset

    def perform_create(self, serializer):
        delivery_group = Group.objects.get(name='delivery crew')
        user = serializer.save()
        user.groups.add(delivery_group)


class crewSingleView(generics.RetrieveDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        delivery_group = Group.objects.get(name='delivery crew')
        queryset = User.objects.filter(groups=delivery_group)
        return queryset
    
class customerCartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)

    def perform_create(self, serializer):
        menuitem = self.request.data.get('menuitem')
        quantity = self.request.data.get('quantity')
        unit_price = MenuItem.objects.get(pk=menuitem).price
        quantity = int(quantity)
        price = quantity * unit_price
        serializer.save(user=self.request.user, price=price)

    def delete(self, request):
        user = self.request.user
        Cart.objects.filter(user=user).delete()
    
class ordersView(generics.ListCreateAPIView):
    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def perform_create(self, serializer):
        cart_items = Cart.objects.filter(user=self.request.user)
        total = self.calculate_total(cart_items)
        order = serializer.save(user=self.request.user, total=total)

        for cart_item in cart_items:
            OrderItem.objects.create(menuitem=cart_item.menuitem, quantity=cart_item.quantity,
                                     unit_price=cart_item.unit_price, price=cart_item.price, order=order)
            cart_item.delete()

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='manager').exists():
            return Order.objects.all()
        return Order.objects.filter(user=user)


    def calculate_total(self, cart_items):
        total = Decimal(0)
        for item in cart_items:
            total += item.price
        return total


class singleOrderView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='manager').exists():
            return Order.objects.all()
        return Order.objects.filter(user=user)
