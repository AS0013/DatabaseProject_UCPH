# Trying GraphQL 

# import graphene
# from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
# from app import db, Project as ProjectModel, Author as AuthorModel, Supervisor as SupervisorModel, Writes as WritesModel, Supervises as SupervisesModel

# class Project(SQLAlchemyObjectType):
#     class Meta:
#         model = ProjectModel
#         interfaces = (graphene.relay.Node, )

# class Author(SQLAlchemyObjectType):
#     class Meta:
#         model = AuthorModel
#         interfaces = (graphene.relay.Node, )

# class Supervisor(SQLAlchemyObjectType):
#     class Meta:
#         model = SupervisorModel
#         interfaces = (graphene.relay.Node, )


# class Query(graphene.ObjectType):
#     node = graphene.relay.Node.Field()
#     all_projects = SQLAlchemyConnectionField(Project.connection)
#     all_authors = SQLAlchemyConnectionField(Author.connection)
#     all_supervisors = SQLAlchemyConnectionField(Supervisor.connection)

# schema = graphene.Schema(query=Query)