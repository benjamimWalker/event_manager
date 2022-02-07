import graphene
from starlette_graphene3 import GraphQLApp
from app.graphql.queris.query import Query
from app.graphql.mutations.mutation import Mutation


graphql_schema = graphene.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLApp(
    schema=graphql_schema,
)