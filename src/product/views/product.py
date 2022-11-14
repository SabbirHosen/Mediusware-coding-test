from django.db.models import Prefetch, Q, QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.views.generic import ListView, CreateView, UpdateView
from ..models import Variant, Product, ProductVariantPrice, ProductVariant
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context


def product_view(request):
    paginated_by = 4
    query_variants = Variant.objects.all()
    select_variants = {}
    for var in query_variants:
        product_variants = ProductVariant.objects.filter(variant=var).values('variant_title').distinct()
        temp = []
        for product_variant in product_variants:
            temp.append(product_variant['variant_title'])
        select_variants[var.title] = temp

    if request.method == 'POST':
        title = request.POST.get('title')
        variant = request.POST.get('variant')
        price_to = request.POST.get('price_to')
        price_from = request.POST.get('price_from')
        date = request.POST.get('date')
        query = ProductVariantPrice.objects.all()
        if title:
            query = query.filter(product_id__title__icontains=title)
        if variant:
            query = query.filter(Q(product_variant_one__variant_title__icontains=variant) |
                                 Q(product_variant_two__variant_title__icontains=variant) |
                                 Q(product_variant_three__variant_title__icontains=variant)
                                 )
        if price_from:
            query = query.filter(price__gte=int(price_from))
        if price_to:
            query = query.filter(price__lte=int(price_to))
        if date:
            year, month, day = str(date).split('-')
            query = query.filter(product_id__created_at__year=year, product_id__created_at__month=month,
                                 product_id__created_at__day=day)
        distinct_product = query.values('product').distinct()
        product_list = []
        for product_id in distinct_product:
            p_id = product_id['product']
            product = Product.objects.get(id=p_id)
            variants = query.filter(product_id=p_id)
            variants_list = []
            try:
                for v in variants:
                    temp = {
                        'variant': f'{v.product_variant_one.variant_title}/{v.product_variant_two.variant_title}/{v.product_variant_three.variant_title}',
                        'price': v.price,
                        'in_stock': v.stock,
                    }
                    # print(temp)
                    variants_list.append(temp)
            except:
                continue

            temp1 = {
                'id': p_id,
                'title': product.title,
                'description': product.description,
                'variants_list': variants_list,
                'created_at': product.created_at
            }
            product_list.append(temp1)
        page = request.GET.get('page', 1)
        paginator = Paginator(product_list, paginated_by)
        try:
            p_product_list = paginator.page(page)
        except PageNotAnInteger:
            p_product_list = paginator.page(1)
        except EmptyPage:
            p_product_list = paginator.page(paginator.num_pages)

        return render(request, template_name='products/list.html',
                      context={'product_list': p_product_list, 'variants': select_variants})
    else:
        # print(select_variants)
        products = Product.objects.all()
        product_list = []
        for product in products:
            variants = ProductVariantPrice.objects.filter(product=product)
            variants_list = []
            try:
                for v in variants:
                    temp = {
                        'variant': f'{v.product_variant_one.variant_title}/{v.product_variant_two.variant_title}/{v.product_variant_three.variant_title}',
                        'price': v.price,
                        'in_stock': v.stock,
                    }
                    # print(temp)
                    variants_list.append(temp)
            except:
                continue
            temp1 = {
                'id': product.id,
                'title': product.title,
                'description': product.description,
                'variants_list': variants_list,
                'created_at': product.created_at
            }
            product_list.append(temp1)
            page = request.GET.get('page', 1)
            paginator = Paginator(product_list, paginated_by)
            try:
                p_product_list = paginator.page(page)
            except PageNotAnInteger:
                p_product_list = paginator.page(1)
            except EmptyPage:
                p_product_list = paginator.page(paginator.num_pages)
            # print(p_product_list.has_next())
        return render(request, template_name='products/list.html',
                      context={'product_list': p_product_list, 'variants': select_variants})


def save_product(request):
    if request.method == "POST":
        response = HttpResponse("Here's the text of the web page.")
        print('hello')
        return response
