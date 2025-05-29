from pydantic import BaseModel

class TemplateResponse(BaseModel):
    template_name: str
    notification_type: str
    language: str
    subject: str | None
    body: str
    placeholders: dict


class UpdateTemplate(BaseModel):
    body: str
    subject: str | None = None  # Optional for emails