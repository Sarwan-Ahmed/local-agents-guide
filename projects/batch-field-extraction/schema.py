"""The fields to extract from each record. Adapt this to your own document type --
extract_batch.py builds its prompt from this schema automatically, so this is the
only file you need to change to extract different fields.
"""

from pydantic import BaseModel


class CustomerRecord(BaseModel):
    full_name: str
    date_of_birth: str | None
    account_number: str | None
    email: str | None
    phone: str | None
