from datetime import datetime, timedelta
from pathlib import Path

import jwt
from cryptography.hazmat.primitives import serialization


def generate_jwt():
    now = datetime.utcnow()
    payload = {
        'iss': "https://auth.payment-service.io/",
        'sub': '73bf3088-0d21-4faf-8491-f576d7bbb758',
        'aud': 'http://127.0.0.1:8000/orders',
        'iat': now.timestamp(),
        'exp': (now + timedelta(hours=24)).timestamp(),
        'scope': "openid"
    }
    private_key_text = Path("private_key.pem").read_text()
    private_key = serialization.load_pem_private_key(
        private_key_text.encode(),
        password=None,
    )
    return jwt.encode(payload=payload, key=private_key, algorithm='RS256')


print(generate_jwt())
