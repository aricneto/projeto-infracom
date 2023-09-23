class Commands:
    LOGIN_CMD = "hi, meu nome eh "
    LOGOUT_CMD = "/bye"
    SHOW_LIST_CMD = "/list"
    SHOW_FRIEND_LIST_CMD = "/mylist"
    ADD_FRIEND_CMD = "/addtomylist "
    REMOVE_FRIEND_CMD = "/rmvfrommylist "
    BAN_CMD = "/ban "
    USER_ENTERED = " entrou na sala!"
    USER_ALREADY_EXISTS = "ja existe um usuario com este nome"
    USER_BANNED = "você foi banido!"

class Ban:
    def __init__(self, banned_user, votes_needed, caller, votes_count=1) -> None:
        self.user = banned_user
        self.votes_count = votes_count
        self.votes_needed = votes_needed
        self.voters = [caller]