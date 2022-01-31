import graphene

from starlette_graphene3 import GraphQLApp

from .query import Query

from .mutation import Mutation


graphql_schema = graphene.Schema(query=Query)

graphql_app = GraphQLApp(
    schema=graphql_schema,
)