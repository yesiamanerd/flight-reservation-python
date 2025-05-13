# To handle operations related to the FlightReservation and related tables.
import mysql.connector
from config.database_config import get_db_connection

# Task 8: Complete the implementation of the ReservationRepository class
class ReservationRepository:
    def __init__(self):
        self.connection = get_db_connection()
        self.cursor = self.connection.cursor()