from django_tenants.postgresql_backend.base import DatabaseWrapper as  TenantDBWrapper
from django.contrib.gis.db.backends.postgis.base import DatabaseWrapper as PostGISDatabaseWrapper

class DatabaseWrapper(TenantDBWrapper):
    SchemaEditorClass = PostGISDatabaseWrapper.SchemaEditorClass
    creation_class = PostGISDatabaseWrapper.creation_class
    features_class = PostGISDatabaseWrapper.features_class
    introspection_class = PostGISDatabaseWrapper.introspection_class
    ops_class = PostGISDatabaseWrapper.ops_class