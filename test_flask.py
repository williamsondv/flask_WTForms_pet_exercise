from unittest import TestCase

from app import app
from models import Pet, db

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/pets_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False


db.drop_all()
db.create_all()


class PetTestCase(TestCase):
    """Tests for views for Pets."""

    def setUp(self):
        """Add sample pet"""
        
        Pet.query.delete()
        
        pet = Pet(name = "pet_name",
        species = "porcupine",
        age = 15,
        notes = "notes test notes test",
        available = True)
       
        db.session.add(pet)
        db.session.commit()

        self.id = pet.id


    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_root(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('pet_name', html)
            

    def test_edit_pet(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('pet_name', html)

            d = {"img_url": "https://static-00.iconduck.com/assets.00/paw-icon-512x449-mbgb3633.png",
                  "notes": "These are my test notes",
                  "available": "true"}
            
            resp = client.post(f"/{self.id}", data=d, follow_redirects=True)
            html= resp.get_data(as_text=True)

            self.assertIn(f"pet_name information updated!", html)

    def test_add_pet(self):
        with app.test_client() as client:
            resp = client.get('/add')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Pet Name", html)
            self.assertIn("Pet Photo URL", html)

            d =     {"name":"new_pet_name",
                    "species":"dog",
                    "age":"10",
                    "img_url": "https://static-00.iconduck.com/assets.00/paw-icon-512x449-mbgb3633.png",
                    "notes": "These are my test notes",
                    "available": "true"}
            resp = client.post(f"/add", data=d, follow_redirects=True)
            html= resp.get_data(as_text=True)

            self.assertIn("new_pet_name", html)
    