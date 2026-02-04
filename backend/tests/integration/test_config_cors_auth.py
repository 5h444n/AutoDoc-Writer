from app.core.config import settings


from app.services.github_service import GitHubService


def test_auth_login_root_exists(client):
    # Call the service directly to validate redirect URL and avoid following external redirects
    resp = GitHubService.get_login_redirect()
    assert resp.status_code in (302, 307)
    loc = resp.headers.get("location")
    assert settings.GITHUB_AUTH_URL in loc


def test_cors_allows_configured_origin(client):
    # Take the first origin from settings and ensure Access-Control-Allow-Origin is set
    origins = getattr(settings, "BACKEND_CORS_ORIGINS", "http://localhost:5173")
    if isinstance(origins, str):
        origins = [o.strip() for o in origins.split(",") if o.strip()]
    origin = origins[0]

    resp = client.get("/", headers={"Origin": origin})
    # CORS middleware should reflect allowed origin
    assert resp.headers.get("access-control-allow-origin") == origin
