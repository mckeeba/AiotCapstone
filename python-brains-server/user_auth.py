import boto3

# AWS Cognito & Identity Pool Details
USER_POOL_ID = "us-east-1_YREP5IfxE"  # Replace with your User Pool ID
CLIENT_ID = "69f24j17t7k18eoji251dauinu"  # Replace with your Cognito App Client ID
IDENTITY_POOL_ID = "us-east-1:cdc8955a-ee68-4f43-844c-cfebae009e0d"  # From Cognito Identity Pool
REGION = "us-east-1"
cognito_client = boto3.client("cognito-idp", region_name=REGION)

# User Login Credentials

def authenticate_user():
    """Authenticate the user with Cognito and get an ID token."""
    email = input("Enter email:")
    password = input("Enter password:")
    try:
        response = cognito_client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": email, "PASSWORD": password},
        )
        token = response["AuthenticationResult"]["IdToken"]
        print("Authentication successful!")
        return token
    except cognito_client.exceptions.NotAuthorizedException:
        print("Incorrect email or password.")
        authenticate_user()
    except cognito_client.exceptions.UserNotFoundException:
        print("User not found.")
        authenticate_user()
    except Exception as e:
        print("Authentication failed:", str(e))
    return None

def register_user():
    """Register a new user in AWS Cognito."""
    password = None
    password_repeat = None
    email = input("Please enter email:")

    while username_taken(email):
        email = input("Username taken. Please enter email:")

    print("\nPasswords must fulfill the following requirements: \n"
                     "- contain at least 6 characters \n"
                     "- have at least one uppercase letter \n"
                     "- have at least one lowercase letter \n"
                     "- have at least one digit and a special letter \n")
    match = False
    while not match:
        password = input("Please enter preferred password: ")
        password_repeat = input("Please re-enter new password:")
        if password != password_repeat:
            print("Passwords do not match.")
        else:
            match = True

    try:
        response = cognito_client.sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            Password=password,
            UserAttributes=[
                {"Name": "email", "Value": email}
            ]
        )
        print(f"User {email} registered successfully! A confirmation code has been sent to your email.")
        confirm_user(email)
        print("Registration complete. Please log in.\n")
        token = authenticate_user()
        return token
    except cognito_client.exceptions.UsernameExistsException as e:
        print("User already exists:", str(e))
        register_user()
    except cognito_client.exceptions.InvalidPasswordException as e:
        print(f"Password policy violation: {str(e)}")
        register_user()
    except Exception as e:
        print("Registration failed:", str(e))
    return False

def username_taken(email):
    """Check if a username (email) already exists in Cognito User Pool."""
    try:
        users = cognito_client.list_users(UserPoolId=USER_POOL_ID)
        for user in users.get("Users", []):
            for attr in user.get("Attributes", []):
                if attr["Name"] == "email" and attr["Value"] == email:
                    return True
    except Exception as e:
        print("Error checking usernames:", str(e))
    return False

def confirm_user(email):
    """Confirm user registration with verification code."""
    confirmation_code = input("Enter the confirmation code sent to your email: ")

    try:
        cognito_client.confirm_sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            ConfirmationCode=confirmation_code,
        )
        print("User confirmed successfully!")
        return True
    except cognito_client.exceptions.CodeMismatchException as e:
        print("Incorrect confirmation code.")
        confirm_user(email)
    except Exception as e:
        print("Confirmation failed:", str(e))
    return False

def get_aws_credentials(id_token):
    """Exchange the Cognito ID token for temporary AWS credentials."""
    identity_client = boto3.client("cognito-identity", region_name=REGION)

    try:
        # Step 1: Get Cognito Identity ID
        identity_response = identity_client.get_id(
            IdentityPoolId=IDENTITY_POOL_ID,
            Logins={f"cognito-idp.{REGION}.amazonaws.com/{USER_POOL_ID}": id_token},
        )
        identity_id = identity_response["IdentityId"]

        # Step 2: Get Temporary AWS Credentials
        cred_response = identity_client.get_credentials_for_identity(
            IdentityId=identity_id,
            Logins={f"cognito-idp.{REGION}.amazonaws.com/{USER_POOL_ID}": id_token},
        )
        print("Temporary AWS Credentials retrieved!")
        return cred_response["Credentials"]

    except Exception as e:
        print("Failed to get AWS credentials:", str(e))
        return None

def retrieve_secret(aws_credentials, secret_name):
    """Retrieve a secret from AWS Secrets Manager using temporary credentials."""
    session = boto3.Session(
        aws_access_key_id=aws_credentials["AccessKeyId"],
        aws_secret_access_key=aws_credentials["SecretKey"],
        aws_session_token=aws_credentials["SessionToken"],
    )

    secrets_client = session.client("secretsmanager", region_name=REGION)

    try:
        secret_response = secrets_client.get_secret_value(SecretId=secret_name)
        print("Secret retrieved successfully!")
        return secret_response["SecretString"]

    except Exception as e:
        print("Failed to retrieve secret:", str(e))
        return None

if __name__ == "__main__":
    id_token = False
    choice = input("Login or Register?(L/R):")
    if choice == "R":
        register_user()
    elif choice == "L":
        id_token = authenticate_user()
    else:
        print("Invalid input!")
        pass

    if id_token:
        aws_credentials = get_aws_credentials(id_token)

        if aws_credentials:
            secret_value = retrieve_secret(aws_credentials, "python-brains-server/aiot_gpt/chat_gpt-api-key")
            print("🔑 Secret Value:", secret_value)
