class SearchView(View):

    def get(self, request):
        data = request.GET.get('search', None)

        try:
            if len(data) > 2:
                recipe_data = list(Recipe.objects.values().filter(Q(title__icontains=data)))
                product_data = list(Product.objects.values().filter(Q(name__icontains=data)))
                return JsonResponse({"SUCCESS": f'recipe_data : {recipe_data} + product_data : {product_data}'},
                                    status=200)

        except:
            return HttpResponse(status=400)
