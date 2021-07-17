from aws_cdk import core

from oedi import __version__
from oedi.config import OEDIConfigBase
from oedi.AWS.data_lake.construct import AWSDataLakeConstruct


class AWSDataLakeStack(core.Stack):
    """AWS data lake stack class"""

    def __init__(self, scope: core.Construct, config: OEDIConfigBase) -> None:
        """Lauch AWS data lake related infrastructures."""
        super().__init__(scope, config.datalake_name, env={
            "region": config.region_name
        })

        for database in config.databases:
            db_name = database["Name"].replace("-", "_")
            data_lake = AWSDataLakeConstruct(
                scope=self,
                id=f"oedi-data-lake-construct-{database['Name']}",
                database_name=db_name,
                version=__version__
            )
            data_lake.create_database()
            data_lake.create_crawler_role()
            #TODO: data_lake.create_workgroup()
            for dataset_location in database['Locations']:
                data_lake.create_crawler(location=dataset_location)
