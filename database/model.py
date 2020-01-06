from sqlalchemy import MetaData

metadata = MetaData(naming_convention={
        "ix": "%(column_0_label)s_ix",
        "uq": "%(table_name)s_%(column_0_name)s_uk",
        "ck": "%(table_name)s_%(constraint_name)s_ck",
        "fk": "%(table_name)s_%(column_0_name)s_%(referred_table_name)s_fk",
        "pk": "%(table_name)s_pk"
    })
