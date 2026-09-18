from banking.database import Base, engine
from banking import models

if __name__ == '__main__':
    Base.metadata.create_all(engine)
