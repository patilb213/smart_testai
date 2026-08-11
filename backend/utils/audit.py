import hashlib
import json
from datetime import datetime
from models.models import db, AuditLog

def write_audit_log(action, user, entity_type, entity_id=None, before_state=None, after_state=None, ip_address=None):
    # Get the last log entry to chain the hash
    last_entry = AuditLog.query.order_by(AuditLog.id.desc()).first()
    previous_hash = last_entry.hash if last_entry else "0" * 64

    entry_data = {
        "action": action,
        "user": user,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "before_state": before_state,
        "after_state": after_state,
        "ip_address": ip_address,
        "timestamp": datetime.utcnow().isoformat(),
        "previous_hash": previous_hash,
    }

    entry_hash = hashlib.sha256(
        (previous_hash + json.dumps(entry_data, sort_keys=True, default=str)).encode()
    ).hexdigest()

    log = AuditLog(
        action=action,
        user=user,
        entity_type=entity_type,
        entity_id=entity_id,
        before_state=before_state,
        after_state=after_state,
        ip_address=ip_address,
        timestamp=datetime.utcnow(),
        previous_hash=previous_hash,
        hash=entry_hash,
    )
    db.session.add(log)
    db.session.commit()
    return log