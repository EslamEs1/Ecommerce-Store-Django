from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from .models import Product, Category, Brand, Review, Wishlist
from taggit.models import Tag
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required

class ProductList(ListView):
    template_name = 'products/list.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = super(ProductList, self).get_queryset()
        
        slug = self.kwargs.get('slug')
        min_price = self.kwargs.get('min')
        max_price = self.kwargs.get('max')
        search_query = self.request.GET.get('q', '')

        if slug:
            queryset = queryset.filter(Q(category__slug=slug) | Q(brand__slug=slug))

        if min_price and max_price:
            queryset = queryset.filter(price__range=(min_price, max_price))

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['pro_slider'] = Product.objects.filter()[:6]
        context['brand'] = Brand.objects.all().annotate(count=Count('product_brand'))
        context['tags'] = Tag.objects.annotate(num_products=Count('product')).filter(num_products=1)
        return context
    


class ProductDetail(DetailView):
    template_name = 'products/detail.html'
    model = Product
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['related'] = Product.objects.filter(category=self.get_object().category).exclude(id=self.get_object().id)
        context['category'] = Category.objects.all()
        context['brand'] = Brand.objects.annotate(count=Count('product_brand'))
        context['tags'] = Tag.objects.annotate(num_products=Count('product')).filter(num_products=1)
        return context
    
    def post(self, request, *args, **kwargs):
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        if request.method == 'POST':
            if comment:
                if not rating:
                    rating = 0
                if Review.objects.filter(user=request.user).exists():
                    messages.error(request, 'Your Already Added Comment')
                    return redirect(request.path)
                else:
                    Review.objects.create(product=self.get_object(), user=request.user, rating=rating, review=comment)
                    messages.success(request, 'Your Rating Added Successful!')
                    return redirect(request.path)
            else:
                messages.error(request, 'Invalid Comment')


@login_required
def wishlist(request):
    try:
        wishlist = Wishlist.objects.get(user=request.user)
        product = wishlist.products.all()
    except Wishlist.DoesNotExist:
        product = []

    if request.method == 'POST':
        id = request.POST.get('wishlist')
        if id:
            try:
                wishlist = Wishlist.objects.get(user=request.user)
                if Product.objects.get(id=id) in wishlist.products.all():
                    wishlist.products.remove(Product.objects.get(id=id))
                    messages.success(request, 'Product removed from wishlist.')
            except (Product.DoesNotExist, Wishlist.DoesNotExist):
                pass

    context = {'wishlist': product}
    return render(request, 'products/wishlist.html', context)


@login_required
def toggle_wishlist(request, slug):
    product = Product.objects.get(slug=slug)

    try:
        wishlist = Wishlist.objects.get(user=request.user)
    except Wishlist.DoesNotExist:
        wishlist = Wishlist.objects.create(user=request.user)

    if product in wishlist.products.all():
        wishlist.products.remove(product)
        messages.success(request, 'Product removed from wishlist.')
    else:
        wishlist.products.add(product)
        messages.success(request, 'Product added to wishlist.')

    return redirect('products:list')
