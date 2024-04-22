import pytest



@pytest.fixture()
def setup():
    # code to tear down test environm
    pass


@pytest.fixture()
def teardown():
    # code to tear down test environment
    pass


@pytest.mark.usefixtures("setup", "teardown")
@pytest.mark.order(1)
def test_create_teacher():

    from fastapi.testclient import TestClient
    from mainapp.main import app
    
    test_client = TestClient(app)

    # Create by json
    teacher_body = {
        "firstname": "Richard",
        "lastname": "Roe",
    }

    response = test_client.post(
        "/teachers",
        json=teacher_body,
    )
    response.raise_for_status()
    body = response.json()
    assert body["code"] == 1


    # Create by Model
    from mainapp.domains.school.teacher import models
    Teacher = models.Teacher

    teacher_0 = Teacher(firstname="Daniel", lastname="Walker", description="teacher 0")
    teacher_1 = Teacher(firstname="Sophia", lastname="Garcia", description="teacher 1")
    teacher_2 = Teacher(firstname="Ethan", lastname="Miller", description="teacher 2")
    teacher_3 = Teacher(firstname="Charlotte", lastname="Wilson", description="teacher 3")

    teacher_a = Teacher(firstname="Scarlett", lastname="Lewis", description="teacher a")
    teacher_b = Teacher(firstname="Audrey", lastname="Taylor", description="teacher b")

    teachers = [
        teacher_0, teacher_1, teacher_2, teacher_3,
        teacher_a, teacher_b,
    ]
    for teacher in teachers:
        response = test_client.post(
            "/teachers",
            json=teacher.model_dump(),
        )


@pytest.mark.usefixtures("setup", "teardown")
@pytest.mark.order(2)
def test_read_teachers_all():

    from fastapi.testclient import TestClient
    from mainapp.main import app
    
    test_client = TestClient(app)

    response = test_client.get(
        "/teachers",
    )
    response.raise_for_status()
    body = response.json()
    assert body["code"] == 1
    assert isinstance(body["data"], list)


@pytest.mark.usefixtures("setup", "teardown")
@pytest.mark.order(3)
def test_read_teacher_by_param():

    from fastapi.testclient import TestClient
    from mainapp.main import app

    test_client = TestClient(app)

    from urllib.parse import quote
    teacher_body = {
        "firstname": "Richard",
        "lastname": "Roe",
    }

    teacher_firstname =  teacher_body["firstname"]
    teacher_lastname = teacher_body["lastname"]

    encoded_teacher_firstname = quote(teacher_firstname)
    encoded_teacher_lastname = quote(teacher_lastname)
    response = test_client.get(
        "/teachers",
        params={
            "firstname": encoded_teacher_firstname,
            "lastname": encoded_teacher_lastname,
        },
    )
    response.raise_for_status()
    body = response.json()
    assert body["code"] == 1
    assert body["data"]["firstname"] == teacher_firstname
    assert body["data"]["lastname"] == teacher_lastname


@pytest.mark.usefixtures("setup", "teardown")
@pytest.mark.order(4)
def test_read_teacher_by_id():

    from fastapi.testclient import TestClient
    from mainapp.main import app
    
    test_client = TestClient(app)

    response = test_client.get(
        "/teachers",
    )
    teacher_body = response.json()["data"][0]
    teacher_id = teacher_body["id"]


    response = test_client.get(
        f"/teachers/{teacher_id}",
    )
    response.raise_for_status()
    body = response.json()
    assert body["code"] == 1
    assert body["data"]["id"] == teacher_id


@pytest.mark.usefixtures("setup", "teardown")
@pytest.mark.order(5)
def test_put_teacher():

    from fastapi.testclient import TestClient
    from mainapp.main import app
    
    test_client = TestClient(app)

    response = test_client.get(
        "/teachers",
    )
    teacher_body = response.json()["data"][0]
    teacher_id = teacher_body["id"]


    new_firstname = "Richardey"
    new_lastname = "Roeny"

    response = test_client.put(
        f"/teachers/{teacher_id}",
        json={
            "firstname": new_firstname,
            "lastname": new_lastname,
            "description": "updated",
        }
    )
    response.raise_for_status()
    body = response.json()
    assert body["code"] == 1
    assert body["data"]["id"] == teacher_id
    assert body["data"]["firstname"] == new_firstname
    assert body["data"]["lastname"] == new_lastname


@pytest.mark.usefixtures("setup", "teardown")
@pytest.mark.order(6)
def test_delete_teacher():

    from fastapi.testclient import TestClient
    from mainapp.main import app
    
    test_client = TestClient(app)

    response = test_client.get(
        "/teachers",
    )
    teacher_body = response.json()["data"][0]
    teacher_id = teacher_body["id"]


    response = test_client.delete(
        f"/teachers/{teacher_id}",
    )
    response.raise_for_status()
    body = response.json()
    assert body["code"] == 1