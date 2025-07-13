import graphene
from crm.models import Product  # Adjust import path based on your project structure

class UpdatedProductType(graphene.ObjectType):
    name = graphene.String()
    stock = graphene.Int()

class UpdateLowStockProducts(graphene.Mutation):
    updated_products = graphene.List(UpdatedProductType)
    message = graphene.String()

    def mutate(self, info):
        products = Product.objects.filter(stock__lt=10)
        updated = []

        for product in products:
            product.stock += 10
            product.save()
            updated.append(UpdatedProductType(name=product.name, stock=product.stock))

        return UpdateLowStockProducts(
            updated_products=updated,
            message=f"Restocked {len(updated)} product(s)."
        )

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()

# UpdateLowStockProducts
