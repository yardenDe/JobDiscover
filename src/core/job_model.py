from dataclasses import dataclass
from typing import Optional

@dataclass
class JobModel:
    title: str
    company: str
    location: Optional[str] = None
    url: Optional[str] = None
    platform: Optional[str] = None
    external_id: Optional[str] = None 
    fingerprint: Optional[str] = None