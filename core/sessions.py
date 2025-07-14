# A simple session manager.
from flask import Response, session, redirect
import uuid, datetime

class Session:
    SID: uuid.UUID = uuid.uuid4() 
    expires: datetime = datetime.datetime.now() + datetime.timedelta(minutes=30)
    grace: datetime = expires + datetime.timedelta(seconds=30)
    __data: dict = {}

    def __getitem__(self, name):
        return self.__data[name]
    
    def __setitem__(self, name, value):
        self.__data[name] = value

    def __refresh(self):
        self.SID: uuid.UUID = uuid.uuid4() 
        self.expires: datetime = datetime.datetime.now() + datetime.timedelta(minutes=30)
        self.grace: datetime = self.expires + datetime.timedelta(seconds=30)

class SessionManager:

    __sessionList: list[Session] = []

    def createSession(self) -> Session:

        """
        Creates a new, empty session with a unique SID and returns it.
        """

        self.__sessionList.append(Session())
        return self.__sessionList[-1]
    
    def deleteSession(self, session: str | uuid.UUID | Session) -> None:

        """
        Deletes a session by SID or direct object reference.
        """

        match str(type(session)):

            case 'str' | 'uuid.UUID':
                session = self.find(session)

            case 'core.sessions.Session':
                pass

            case _:
                print("NOT A SESSION!")
                return

        if session in self.__sessionList:
            self.__sessionList.remove(session)
            return
        
        else:
            print("SESSION NOT FOUND!")
            return
        
    def ensureSession(self) -> Response | None:

        """
        Ensures a session exists for the visiting client.
        """

        if 'sid' not in session.keys():
            return redirect('/login')
        
        else: 
            return None
        
    def __getitem__(self, sid) -> Session:

        for sess in self.__sessionList:
            if datetime.datetime.now() > sess.expires:
                if datetime.datetime.now() < sess.grace:
                    sess.__refresh()
                else:
                    self.__sessionList.remove(sess)

            if sess.SID == sid:
                return sess
            
GLOBAL_SESSIONMANAGER = SessionManager()
    