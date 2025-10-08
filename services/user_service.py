from repositories.user_repository import UserRepository
# typically passwords would be hashed. Similarly the sesson management would be more complex.

class UserService:
    
    def __init__(self):
        self.repository = UserRepository()

    def user_login(self, username, password):
        
        user_data = self.repository.authenticate_user(username, password)

        if not user_data:
            return None

        return user_data['role']

    def get_all_users(self):
        users_data = self.repository.get_all_users()

        if not users_data:
            return "No users found in the system."
        
        return users_data