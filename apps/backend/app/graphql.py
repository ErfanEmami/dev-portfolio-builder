import strawberry
from strawberry.fastapi import GraphQLRouter
from app.resolvers import Query

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)
