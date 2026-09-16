# import pytest

# API = "/api"


# async def test_create_department_success(client, admin_token):
#     headers = {"Authorization": f"Bearer {admin_token}"}
#     response = await client.post(
#         f"{API}/admin/departments",
#         json={"name": "Engineering"},
#         headers=headers,
#     )
#     assert response.status_code == 201
#     body = response.json()
#     assert body["data"]["name"] == "Engineering"
#     assert "uuid" in body["data"]


# async def test_create_department_duplicate_name_rejected(client, admin_token):
#     headers = {"Authorization": f"Bearer {admin_token}"}
#     await client.post(f"{API}/admin/departments",
#                       json={"name": "Engineering"}, headers=headers)
#     response = await client.post(f"{API}/admin/departments",
#                                  json={"name": "Engineering"}, headers=headers)
#     assert response.status_code == 409


# async def test_create_department_without_auth_rejected(client):
#     response = await client.post(
#         f"{API}/admin/departments", json={"name": "Engineering"}
#     )
#     assert response.status_code == 401


# async def test_get_department_by_uuid(client, admin_token):
#     headers = {"Authorization": f"Bearer {admin_token}"}
#     create_res = await client.post(
#         f"{API}/admin/departments", json={"name": "Design"}, headers=headers
#     )
#     dept_uuid = create_res.json()["data"]["uuid"]
#     response = await client.get(
#         f"{API}/admin/departments/{dept_uuid}", headers=headers
#     )
#     assert response.status_code == 200
#     assert response.json()["data"]["name"] == "Design"


# async def test_get_department_not_found(client, admin_token):
#     headers = {"Authorization": f"Bearer {admin_token}"}
#     fake_uuid = "00000000-0000-0000-0000-000000000000"
#     response = await client.get(
#         f"{API}/admin/departments/{fake_uuid}", headers=headers
#     )
#     assert response.status_code == 404


# async def test_rename_department_to_own_name_allowed(client, admin_token):
#     headers = {"Authorization": f"Bearer {admin_token}"}
#     create_res = await client.post(
#         f"{API}/admin/departments", json={"name": "Sales"}, headers=headers
#     )
#     dept_uuid = create_res.json()["data"]["uuid"]
#     response = await client.put(
#         f"{API}/admin/departments/{dept_uuid}",
#         json={"name": "Sales"},
#         headers=headers,
#     )
#     assert response.status_code == 200


# async def test_rename_department_to_existing_other_name_rejected(client, admin_token):
#     headers = {"Authorization": f"Bearer {admin_token}"}
#     await client.post(f"{API}/admin/departments",
#                       json={"name": "HR"}, headers=headers)
#     create_res = await client.post(
#         f"{API}/admin/departments", json={"name": "Finance"}, headers=headers
#     )
#     finance_uuid = create_res.json()["data"]["uuid"]
#     response = await client.put(
#         f"{API}/admin/departments/{finance_uuid}",
#         json={"name": "HR"},
#         headers=headers,
#     )
#     assert response.status_code == 409