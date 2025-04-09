"""Example integration using DataUpdateCoordinator."""

import logging

from wakatime_api import ApiClient
from wakatime_api.api.commits_api import CommitsApi
from wakatime_api.api.data_dumps_api import DataDumpsApi
from wakatime_api.api.durations_api import DurationsApi
from wakatime_api.api.external_durations_api import ExternalDurationsApi
from wakatime_api.api.goals_api import GoalsApi
from wakatime_api.api.heartbeats_api import HeartbeatsApi
from wakatime_api.api.insights_api import InsightsApi
from wakatime_api.api.leaderboards_api import LeaderboardsApi
from wakatime_api.api.meta_api import MetaApi
from wakatime_api.api.organizations_api import OrganizationsApi
from wakatime_api.api.projects_api import ProjectsApi
from wakatime_api.api.resources_api import ResourcesApi
from wakatime_api.api.stats_api import StatsApi
from wakatime_api.api.summaries_api import SummariesApi
from wakatime_api.api.users_api import UsersApi

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from . import WakaTimeConfigEntry
from .const import DOMAIN, SCAN_INTERVAL
from .sensor import MyEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, config_entry: WakaTimeConfigEntry, async_add_entities
):
    """WakaTime config entry."""
    client = hass.data[DOMAIN][config_entry.data["client"]]
    coordinator = WakaTimeCoordinator(hass, config_entry, client)

    await coordinator.async_config_entry_first_refresh()

    async_add_entities(
        MyEntity(coordinator, idx) for idx, ent in enumerate(coordinator.data)
    )


class WakaTimeCoordinator(DataUpdateCoordinator):
    """WakaTime integration coordinator."""

    def __init__(
        self, hass: HomeAssistant, config_entry: WakaTimeConfigEntry, client: ApiClient
    ) -> None:
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="WakaTime",
            config_entry=config_entry,
            update_interval=SCAN_INTERVAL,
            # Set always_update to `False` if the data returned from the
            # api can be compared via `__eq__` to avoid duplicate updates
            # being dispatched to listeners
            always_update=True,
        )
        self.client = client
        self._commits_api: CommitsApi | None = None
        self._data_dumps_api: DataDumpsApi | None = None
        self._durations_api: DurationsApi | None = None
        self._external_durations_api: ExternalDurationsApi | None = None
        self._goals_api: GoalsApi | None = None
        self._heartbeats_api: HeartbeatsApi | None = None
        self._insights_api: InsightsApi | None = None
        self._leaderboards_api: LeaderboardsApi | None = None
        self._meta_api: MetaApi | None = None
        self._organizations_api: OrganizationsApi | None = None
        self._projects_api: ProjectsApi | None = None
        self._resources_api: ResourcesApi | None = None
        self._stats_api: StatsApi | None = None
        self._summaries_api: SummariesApi | None = None
        self._users_api: UsersApi | None = None

    async def _async_setup(self):
        """Set up the coordinator."""
        self._commits_api = CommitsApi(self.client)
        self._data_dumps_api = DataDumpsApi(self.client)
        self._durations_api = DurationsApi(self.client)
        self._external_durations_api = ExternalDurationsApi(self.client)
        self._goals_api = GoalsApi(self.client)
        self._heartbeats_api = HeartbeatsApi(self.client)
        self._insights_api = InsightsApi(self.client)
        self._leaderboards_api = LeaderboardsApi(self.client)
        self._meta_api = MetaApi(self.client)
        self._organizations_api = OrganizationsApi(self.client)
        self._projects_api = ProjectsApi(self.client)
        self._resources_api = ResourcesApi(self.client)
        self._stats_api = StatsApi(self.client)
        self._summaries_api = SummariesApi(self.client)
        self._users_api = UsersApi(self.client)
