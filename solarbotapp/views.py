import jwt,os,sys
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from .serializers import *
from django.contrib import messages
from django.utils import timezone as dt
from rest_framework.pagination import PageNumberPagination
from django.db.models import F

class create_product(APIView):
    def post(self,request):
        try:
            product = products()
            serializer = create_product_serializer(data=request.data)
            image = request.FILES['image']
            file_upload = request.FILES.getlist('file_upload')
            if not image.name.endswith('.jpeg'):
                return Response({
                    "message":"Wrong Image Format"
                    }, status=status.HTTP_400_BAD_REQUEST)
            # if not image.name.endswith('.jpeg'):
            #     return Response({
            #         "message":"Wrong Image Format"
            #         }, status=status.HTTP_400_BAD_REQUEST)
            # if not image.name.endswith('.png'):
            #     return Response({
            #         "message":"Wrong Image Format"
            #         }, status=status.HTTP_400_BAD_REQUEST)
            
            product_description_ = request.data.get('product_description')
            if serializer.is_valid(raise_exception=True):
                product.product_code = serializer.validated_data['product_code']
                product.product_name = serializer.validated_data['product_name']
                product.product_description = product_description_
                product.image = image
                for file_ in file_upload:
                    product_file(files=file_,product_code = serializer.validated_data['product_code']).save()
                product.vendor_name = serializer.validated_data['vendor_name']
                product.category = serializer.validated_data['category']
                product.sub_category = serializer.validated_data['sub_category']
                product.retail_price = serializer.validated_data['retail_price']
                product.cost_price = serializer.validated_data['cost_price']
                product.quantity = serializer.validated_data['quantity']
                product.created_time = dt.now()
                product.state_manager = None
                product.save()
                return Response({
                    'message':'Added Product Successfully'
                },status=status.HTTP_200_OK)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return Response({
                # "message": serializer.errors,
                "message": str(e),
                "lno": exc_tb.tb_lineno
            }, status=status.HTTP_400_BAD_REQUEST)

class list_product(APIView,PageNumberPagination):
    def get(self,request, *args, **kwargs):
        try:
            productQuesryset = products.objects.filter(state_manager__isnull=True).order_by('-created_time')
            product_code = request.GET.get('product_code')
            product_description = request.GET.get('product_description')
            category = request.GET.get('category')
            product_group = request.GET.get('product_group')
            category_ = request.GET.get('category_')
            quantity = request.GET.get('quantity')
            product_code_sort_order = request.GET.get('product_code_sort_order')
            quantity_sort_order = request.GET.get('quantity_sort_order')
            category_sort_order = request.GET.get('category_sort_order')
            product_group_sort_order = request.GET.get('product_group_sort_order')
            product_description_sort_order = request.GET.get('product_description_sort_order')
            size = request.GET.get('size')
            page = request.GET.get('page')

            if product_code:
                productQuesryset=productQuesryset.filter(product_code__icontains=product_code).order_by('-created_time')
            if product_description:
                productQuesryset=productQuesryset.filter(product_description__icontains=product_description).order_by('-created_time')
            if category:
                productQuesryset=productQuesryset.filter(category__icontains=category).order_by('-created_time')
            if product_group:
                productQuesryset=productQuesryset.filter(product_group__icontains=product_group).order_by('-created_time')
            
            if category_ is not None:
                productQuesryset=productQuesryset.filter(state_manager__isnull=True,category=category_).order_by('-created_time')
            else:
                productQuesryset=productQuesryset.filter(state_manager__isnull=True).order_by('-created_time')  
            
            if quantity is not None:
                quantity = int(quantity)
                if (quantity >= 0) and (quantity <= 100):
                    productQuesryset=productQuesryset.filter(quantity__range=[0,100]).order_by('-created_time')
                elif (quantity >=101) and (quantity <= 200):
                    productQuesryset=productQuesryset.filter(quantity__range=[100,200]).order_by('-created_time')
                elif (quantity >=201) and (quantity <= 300):
                    productQuesryset=productQuesryset.filter(quantity__range=[200,300]).order_by('-created_time')
                elif (quantity >=301) and (quantity <= 400):
                    productQuesryset=productQuesryset.filter(quantity__range=[300,400]).order_by('-created_time')
                else:
                    productQuesryset=productQuesryset.filter(quantity__gt=400).order_by('-created_time')
            
            if  product_code_sort_order == 'desc':
                productQuesryset=productQuesryset.filter(state_manager__isnull=True).order_by('-product_code')
            elif product_code_sort_order == 'asc':
                productQuesryset=productQuesryset.filter(state_manager__isnull=True).order_by('product_code')
                
            if  quantity_sort_order == 'desc':
                productQuesryset=productQuesryset.filter(state_manager__isnull=True).order_by(F('quantity').desc(nulls_last=True),F('id'))
            elif quantity_sort_order == 'asc':
                productQuesryset=productQuesryset.filter(state_manager__isnull=True).order_by(F('quantity').asc(nulls_last=True),F('id'))
                
            if category_sort_order == 'desc':
                productQuesryset=productQuesryset.filter(state_manager__isnull=True).order_by('-category')
            elif category_sort_order == 'asc':
                productQuesryset=productQuesryset.filter(state_manager__isnull=True).order_by('category')
            
            if product_group_sort_order == 'desc':    
                productQuesryset=productQuesryset.filter(state_manager__isnull=True).order_by('-product_group')
            elif product_group_sort_order == 'asc':
                productQuesryset=productQuesryset.filter(state_manager__isnull=True).order_by('product_group')
                
            if product_description_sort_order == 'desc':
                productQuesryset=productQuesryset.filter(state_manager__isnull=True).order_by('-product_description')
            elif product_description_sort_order == 'asc':
                productQuesryset=productQuesryset.filter(state_manager__isnull=True).order_by('product_description')
                
            self.page_size_query_param = 'size'
            page = self.paginate_queryset(productQuesryset, request)
            print(page)

            serializer=product_list_serializer(page, many=True)
            
            return Response({
                'message':"Product List",
                'data':serializer.data,
                'current': self.page.number,
                'total_pages':self.page.paginator.num_pages,
            },status=status.HTTP_200_OK)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return Response({
                "message": str(e),
                "lno": exc_tb.tb_lineno
            }, status=status.HTTP_400_BAD_REQUEST)

class get_product_details(APIView):
    def get(self,request, **kwargs):
        try:
            id = kwargs.get('id')
            product = products.objects.get(id=id)
            product.updated_time = dt.now()
            serializer=product_detail_serializer(product)
            return Response({
                "message":"Product Details",
                "data":serializer.data
            },status=status.HTTP_200_OK)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return Response({
                "message": str(e),
                "lno": exc_tb.tb_lineno
            }, status=status.HTTP_400_BAD_REQUEST)

class edit_product(APIView):
    def put(self, request, id,*args, **kwargs):
        try:
            instance = products.objects.get(id=id)
            serializer = update_product_serializer(instance=instance, data=request.data)
            if serializer.is_valid():
                serializer.update_(instance=instance,validated_data=serializer.validated_data)
                return Response({"message":"Updated Candidate Details",
                                "data":serializer.data
                            }, status=status.HTTP_200_OK)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return Response({
                "message": str(e),
                "lno": exc_tb.tb_lineno
            }, status=status.HTTP_400_BAD_REQUEST)