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
                self.client = MongoClient(mongodb_uri)
                self.database = self.client[database_name]
                # Test the connection
                self.client.admin.command('ping')
                print("Successfully connected to MongoDB Atlas")
            except Exception as e:
                raise ConnectionError(f"Failed to connect to MongoDB: {str(e)}")

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
