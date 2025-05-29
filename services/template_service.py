from fastapi import HTTPException
from sqlalchemy.orm import Session
from db_connection.database import get_db
from db_connection.notification_model import NotificationTemplate
from models.template_models import UpdateTemplate


def handle_getting_all_templates(notification_type: str = None):
    db: Session = next(get_db())
    query = db.query(NotificationTemplate)
    
    if notification_type:
        query = query.filter(NotificationTemplate.notification_type == notification_type)

    templates = query.all()
    templateResponse = [
        {
            "template_name": t.template_name,
            "notification_type": t.notification_type,
            "language": t.language,
            "subject": t.subject,
            "body": t.body,
            "placeholders": t.placeholders
        }
        for t in templates
    ]
    print(templateResponse)
    return templateResponse

def handle_getting_specific_template(template_name: str):
    db: Session = next(get_db())
    template = db.query(NotificationTemplate).filter_by(template_name=template_name).first()

    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    templateResponse = {
        "template_name": template.template_name,
        "notification_type": template.notification_type,
        "language": template.language,
        "subject": template.subject,
        "body": template.body,
        "placeholders": template.placeholders
    }
    print(templateResponse)
    return templateResponse


def handle_update_template(template_name: str, template_update: UpdateTemplate):
    db: Session = next(get_db())
    template = db.query(NotificationTemplate).filter_by(template_name=template_name).first()

    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    template.body = template_update.body
    if template_update.subject:
        template.subject = template_update.subject

    db.commit()
    db.refresh(template)
    return {"message": "Template updated successfully", "updated_template": template}