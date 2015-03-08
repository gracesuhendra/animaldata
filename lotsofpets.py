from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Animal, Base, PetItem
 
engine = create_engine('sqlite:///animalpet.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()



#Pet for Dog
animal1 = Animal(name = "Dog")

session.add(animal1)
session.commit()


petItem1 = PetItem(name = "Sheldon", description = "very cute", gender = "Male", animal = animal1)

session.add(petItem1)
session.commit()

petItem2 = PetItem(name = "Orzo", description = "Jvery funny", gender = "Female", animal = animal1)

session.add(petItem2)
session.commit()


#Pet for Cat
animal2 = Animal(name = "Cat")

session.add(animal2)
session.commit()


petItem1 = PetItem(name = "Allen", description = "super cute", gender = "Male", animal = animal2)

session.add(petItem1)
session.commit()

petItem2 = PetItem(name = "Bunny", description = "super funny", gender = "Female", animal = animal2)

session.add(petItem2)
session.commit()






print "added pet items!"
