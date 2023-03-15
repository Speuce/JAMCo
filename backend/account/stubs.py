def stub_verify_oauth2_token(credential: str, client_id: str) -> dict:
    if credential != "test" or client_id != "test":
        raise ValueError("Invalid Credentials")
    else:
        return {
            "sub": "1234567890",
            "email": "john.doe@gmail.com",
            "picture": "https://i.imgur.com/QJpNyuN.png",
            "given_name": "John",
            "family_name": "Doe",
        }
