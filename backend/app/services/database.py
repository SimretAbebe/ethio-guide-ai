from pymongo import MongoClient
from pymongo.database import Database
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.client: MongoClient = None
        self.database: Database = None

    def connect(self) -> Database:
        """Connect to MongoDB Atlas and return database instance"""
        if self.database is None:
            mongodb_uri = os.getenv("MONGODB_URI")
            database_name = os.getenv("DATABASE_NAME")

            if not mongodb_uri:
                raise ValueError("MONGODB_URI environment variable is not set")

            if not database_name:
                raise ValueError("DATABASE_NAME environment variable is not set")

            try:
                # Mask URI for security but show some part of it to verify it's the right one
                masked_uri = mongodb_uri.split("@")[-1] if "@" in mongodb_uri else "HIDDEN"
                print(f"Attempting to connect to MongoDB cluster: {masked_uri}...")
                
                self.client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
                self.database = self.client[database_name]
                
                # Test the connection
                print(f"Pinging MongoDB database '{database_name}'...")
                self.client.admin.command('ping')
                print("Successfully connected to MongoDB Atlas!")
            except Exception as e:
                error_msg = f"DATABASE CONNECTION ERROR: {str(e)}"
                print(error_msg)
                # Re-raise with full message
                raise ConnectionError(error_msg)

        return self.database

    def close(self):
        """Close the database connection"""
        if self.client:
            self.client.close()
            self.client = None
            self.database = None

# Global database connection instance
db_connection = DatabaseConnection()

def get_database() -> Database:
    """Get database instance"""
    return db_connection.connect()
