from unittest.mock import patch
from app.core.config import settings
from app.models.user import User


def test_login_redirect_uses_settings(client):
    resp = client.get("/api/v1/auth/login")
    assert resp.status_code in (302, 307)
    loc = resp.headers.get("location")
    assert loc is not None
    assert settings.GITHUB_AUTH_URL in loc
    assert f"client_id={settings.GITHUB_CLIENT_ID}" in loc
    assert settings.REDIRECT_URI in loc


def test_get_me_returns_user_profile(client, test_db):
    # Arrange: create a user with an access token
    user = User(github_username="testuser", access_token="valid_token_123")
    test_db.add(user)
    test_db.commit()

    expected = {
        "username": "testuser",
        "name": "Test User",
        "avatar": "https://example.com/avatar.png",
        "email": "test@example.com",
    }

    with patch("app.services.github_service.GitHubService.get_user_details") as mock_get:
        mock_get.return_value = expected

        # Act
        resp = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer valid_token_123"},
        )

        # Assert
        assert resp.status_code == 200
        assert resp.json() == expected
