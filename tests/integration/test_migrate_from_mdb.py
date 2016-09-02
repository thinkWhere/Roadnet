import os
import unittest

# The test migration script isn't in a package directory so add to path
import sys
sys.path.append(os.path.join(os.getcwd(), 'database_files'))
import migrate_from_mdb as mgr8


class DatabaseMigrationTestCase(unittest.TestCase):
    def setUp(self):
        self.output_db_path = mgr8.OUTPUT_DB_PATH
        self.migrator = mgr8.MdbMigrator()

    def tearDown(self):
        if os.path.isfile(mgr8.OUTPUT_DB_PATH):
            os.remove(mgr8.OUTPUT_DB_PATH)

    def test_db_created(self):
        self.migrator.create_new_spatialite_db()
        self.assertTrue(os.path.isfile(self.output_db_path),
                        'No file created at {}'.format(self.output_db_path))

if __name__ == '__main__':
    unittest.main()
