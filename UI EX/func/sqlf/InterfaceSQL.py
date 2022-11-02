import abc

# compatible with Python 2 *and* 3:
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})


class interfaceSQL(ABC):

    @abc.abstractmethod
    def __init__(self, host, user, password, database):
        pass

    @abc.abstractmethod
    def GetConnect(self):
        pass

    @abc.abstractmethod
    def ExecQuery(self, sql):
        pass

    @abc.abstractmethod
    def ExecNonQuery(self, sql):
        pass
