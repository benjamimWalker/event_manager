import graphene
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

class Mutation(graphene.ObjectType):
    pass

class Query(graphene.ObjectType):
    hello = graphene.String(nome=graphene.Argument(type_=graphene.String, required=False))
    
    def resolve_hello(self, info, nome):
        if nome == None:
            return 'hello'
        return f"hello, {nome}!!!"

graphql_schema = graphene.Schema(query=Query)

graphql_app = GraphQLApp(
    schema=graphql_schema,
    on_get=make_graphiql_handler()
)