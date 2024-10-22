"""
Views for the recipe API.
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
)
from drf_spectacular.types import OpenApiTypes

from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag, Ingredient
from recipe import serializers


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(name='tags', type=OpenApiTypes.STR, required=False,
                             location=OpenApiParameter.QUERY,
                             description='Comma separated IDs to filter'),

            OpenApiParameter(name='ingredients', type=OpenApiTypes.STR, required=False,
                             location=OpenApiParameter.QUERY,
                             description='Comma separated IDs to filter',
                             examples=[
                                 OpenApiExample(
                                     name='filter by 2 ingredients',
                                     value='4,7',
                                 ),
                                 OpenApiExample(
                                     name='filter by 1 ingredient',
                                     value='7',
                                 ),
                             ]),
        ],
        # description='More descriptive text.'
        examples=[
            OpenApiExample(
                name='Example 1',
                value={
                    "id": 5,
                    "title": "Chicken soup",
                    "time_minutes": 45,
                    "price": "25.99",
                    "link": "https://example.com/chicken-soup.pdf",
                    "tags": [
                        {
                            "id": 4,
                            "name": "White meat"
                        }
                    ],
                    "ingredients": [
                        {
                            "id": 3,
                            "name": "Pepper"
                        },
                        {
                            "id": 77,
                            "name": "Salt"
                        }
                    ]
                }

            )
        ]
    )
)
class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, qs):
        """Convert a list of strings to integer"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """"""
        # return self.queryset.filter(user=self.request.user).order_by('-id')
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset.filter(user=self.request.user)

        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)

        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.order_by('-id').distinct()

    def get_serializer_class(self):
        """Return the serializer class for the request."""
        if self.action == 'list':
            return serializers.RecipeSerializer

        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to recipe."""
        recipe = self.get_object()
        serializer = self.get_serializer(instance=recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name='assigned_only',
                type=OpenApiTypes.INT,
                enum=[0, 1],
                location=OpenApiParameter.QUERY,
                description='Filter by items assigned to recipes.'
            )
        ]
    )
)
class BaseRecipeAttrViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Base viewset for recipe attributes."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)
        return queryset.filter(user=self.request.user).order_by('-name').distinct()


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in database."""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
