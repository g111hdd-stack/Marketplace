from dataclasses import dataclass


@dataclass
class DataYaCampaigns:
    client_id: str
    campaign_id: str
    name: str
    placement_type: str
