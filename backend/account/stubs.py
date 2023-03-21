from faker import Faker


def stub_verify_oauth2_token(credential: str, client_id: str) -> dict:
    if credential == "test" and client_id == "test":
        return {
            "sub": "1234567890",
            "email": "john.doe@gmail.com",
            "picture": "https://i.imgur.com/QJpNyuN.png",
            "given_name": "John",
            "family_name": "Doe",
        }
    elif credential == "test2" and client_id == "test2":
        return {
            "sub": "0987654321",
            "email": "jane.doe@gmail.com",
            "picture": "https://i.imgur.com/QJpNyuN.png",
            "given_name": "Jane",
            "family_name": "Doe",
        }
    elif credential == "load_test" and client_id == "load_test":
        faker = Faker()
        return {
            "sub": faker.uuid4(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": faker.email(),
        }
    else:
        raise ValueError("Invalid Credentials")
