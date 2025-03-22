# import requests
# import uuid

# BASE_URL = "http://localhost:8081"
# TEST_USER_ID = "11111111-2222-3333-4444-555555555555"
# TEST_FILE_KEY = "67de75eca76bd4020aab2da5"

# headers = {
#     "x-auth-sub": TEST_USER_ID
# }

# def test_download_file():
#     response = requests.get(
#         f"{BASE_URL}/file/{TEST_FILE_KEY}",
#         headers=headers
#     )

#     print("Download response:", response.status_code, response.text)

#     assert response.status_code == 200
#     data = response.json()
#     assert "file_url" in data
#     assert data["file_url"].startswith("https://") or data["file_url"].startswith("http://")