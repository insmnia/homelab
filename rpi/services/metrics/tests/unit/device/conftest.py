from app.domains.device.models import DeviceSQLModel
import factory
from async_factory_boy.factory.sqlalchemy import AsyncSQLAlchemyFactory
from tests.unit.conftest import sc_session


class DeviceFactory(AsyncSQLAlchemyFactory):
    class Meta:
        model = DeviceSQLModel
        sqlalchemy_session = sc_session

    id = factory.Sequence(lambda n: n)
    mac = factory.Faker("mac_address")
    ip = factory.Faker("ipv4_public")
    name = factory.Faker("word")
    description = factory.Faker("sentence")
    is_online = factory.Faker("boolean")
    last_seen_at = factory.Faker("date_time_this_decade", before_now=True, after_now=False, tzinfo=None)
