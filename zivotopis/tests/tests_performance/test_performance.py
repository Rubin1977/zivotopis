import time
import pytest

# Thresholds
HOMEPAGE_MAX = 0.5
EN_PAGE_MAX = 0.5
API_POSTS_MAX = 0.7
CONTACT_FORM_MAX = 0.8

def ascii_bar(seconds):
    # 1 block = 0.05s
    blocks = int(seconds / 0.05)
    return "#" * blocks # ASCII-safe

@pytest.mark.django_db
def test_homepage_performance(client):
    start = time.time()
    response = client.get("/zivo/")
    duration = time.time() - start

    print(f"PERF /zivo/: {duration:.3f}s {ascii_bar(duration)}")

    assert response.status_code == 200
    assert duration < HOMEPAGE_MAX


@pytest.mark.django_db
def test_homepage_en_performance(client):
    start = time.time()
    response = client.get("/en/zivo/")
    duration = time.time() - start

    print(f"PERF /en/zivo/: {duration:.3f}s {ascii_bar(duration)}")

    assert response.status_code == 200
    assert duration < EN_PAGE_MAX


@pytest.mark.django_db
def test_api_posts_performance(client):
    start = time.time()
    response = client.get("/api/posts/")
    duration = time.time() - start

    print(f"PERF /api/posts/: {duration:.3f}s {ascii_bar(duration)}")

    assert response.status_code == 200
    assert duration < API_POSTS_MAX


@pytest.mark.django_db
def test_contact_form_performance(client):
    start = time.time()
    response = client.post("/email/", {
        "name": "Test",
        "email": "test@example.com",
        "message": "Hello"
    })
    duration = time.time() - start

    print(f"PERF /email/: {duration:.3f}s {ascii_bar(duration)}")

    assert response.status_code in (200, 302)
    assert duration < CONTACT_FORM_MAX
