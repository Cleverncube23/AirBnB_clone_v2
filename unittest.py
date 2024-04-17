import unittest
import MySQLdb  # or another MySQL library

# Assuming you have a method to perform an action like creating a new record
def create_new_state():
    # Execute SQL query to add a new state record in the 'states' table
    db = MySQLdb.connect(host='localhost', user='hbnb_test', passwd='hbnb_test_pwd', db='hbnb_test_db')
    cursor = db.cursor()
    cursor.execute("INSERT INTO states (name) VALUES ('California')")
    db.commit()
    db.close()

class TestMySQLStorage(unittest.TestCase):

    def setUp(self):
        # Setup any necessary resources or connections before each test
        pass

    def tearDown(self):
        # Clean up after each test (e.g., remove added records)
        pass

    def test_create_new_state(self):
        # Count records before creating a new state
        db = MySQLdb.connect(host='localhost', user='hbnb_test', passwd='hbnb_test_pwd', db='hbnb_test_db')
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM states")
        count_before = cursor.fetchone()[0]
        db.close()

        # Perform the action to create a new state
        create_new_state()

        # Count records after creating a new state
        db = MySQLdb.connect(host='localhost', user='hbnb_test', passwd='hbnb_test_pwd', db='hbnb_test_db')
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM states")
        count_after = cursor.fetchone()[0]
        db.close()

        # Assert that the number of records increased by 1
        self.assertEqual(count_after, count_before + 1)

if __name__ == '__main__':
    unittest.main()
