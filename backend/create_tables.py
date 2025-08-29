from db import Base, engine
from routers.optimize import Delivery

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")