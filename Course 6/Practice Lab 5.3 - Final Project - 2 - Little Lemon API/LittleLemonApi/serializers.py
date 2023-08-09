from .models import Category,MenuItem,Cart,Order,OrderItem
from rest_framework.serializers import *
from django.contrib.auth.models import User

class CategorySerializer(ModelSerializer):
     class Meta:
         model = Category
         fields = ['id','title']
         
class MenuItemSerializer(ModelSerializer):
    class Meta:
        model=MenuItem
        fields=['id', 'title', 'price', 'category', 'featured']
        
class CartSerializer(ModelSerializer):
    unit_price=DecimalField(source='menuitem.price',max_digits=6,decimal_places=2,read_only=True)
    name=CharField(source='menuitem.title',read_only=True)

    class Meta:
        model=Cart
        fields = ['user_id', 'menuitem', 'name', 'quantity', 'unit_price', 'price']
        extra_kwargs = {
            'price': {'read_only': True}
        }  
        
class UserSerializer(ModelSerializer):
    email = EmailField(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email']

    
class OrderItemSerializer(ModelSerializer):
    unit_price = DecimalField(max_digits=6, decimal_places=2, source='menuitem.price', read_only=True)
    price = DecimalField(max_digits=6, decimal_places=2, read_only=True)
    name = CharField(source='menuitem.title', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['name', 'quantity', 'unit_price', 'price']
        extra_kwargs = {
            'menuitem': {'read_only': True}
        }
    
class OrdersSerializer(ModelSerializer):
    order_items=SerializerMethodField()
    
    class Meta:
        model=Order
        fields=['id','user','delivery_crew','status','total','order_items']
        extra_kwargs = {
            'total': {'read_only': True}
        }
    
    def get_order_items(self, obj):
        order_items = OrderItem.objects.filter(order=obj)
        serializer = OrderItemSerializer(order_items, many=True, context={'request': self.context['request']})
        return serializer.data