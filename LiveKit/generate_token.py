from livekit import api
import os

API_KEY = "devkey"
API_SECRET = "secret"

token = (
    api.AccessToken(API_KEY, API_SECRET)
    .with_identity("user")
    .with_name("User")
    .with_grants(
        api.VideoGrants(
            room_join=True,
            room="test",
            can_publish=True,
            can_subscribe=True,
        )
    )
    .to_jwt()
)

print(token)
