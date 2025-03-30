from models import MessageModel, UserModel

class ChatService:
    def __init__(self):
        self.message_model = MessageModel()
        self.user_model = UserModel()

    def get_messages(self, limit=100):
        """Get the most recent messages"""
        return self.message_model.list_messages(limit)

    def post_message(self, params):
        """Add a new message to the chat"""
        # Ensure the user exists and is up to date
        username = params.get("username")
        color = params.get("color", "#3498db")
        
        # Create or update the user
        user = self.user_model.create_or_update(username, color)
        
        # Create the message with the user's info
        message_params = {
            "content": params.get("content"),
            "username": username,
            "color": user.get("color")
        }
        
        return self.message_model.create(message_params)

    def change_username(self, old_username, new_username):
        """Change a user's username across all messages"""
        return self.user_model.update_username(old_username, new_username)

    def change_color(self, username, color):
        """Change a user's color for display"""
        return self.user_model.update_color(username, color)

    def get_user(self, username):
        """Get a user's information"""
        return self.user_model.get_by_username(username)