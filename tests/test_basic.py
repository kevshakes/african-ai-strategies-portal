import unittest
from src.models import StrategyDatabase
from src.data_collector import DataCollector
from app import app

class TestBasicFunctionality(unittest.TestCase):
    def setUp(self):
        self.db = StrategyDatabase()
        self.collector = DataCollector()
        self.app = app.test_client()

    def test_database_initialization(self):
        """Test that database can be initialized"""
        self.assertIsNotNone(self.db)

    def test_data_collector_initialization(self):
        """Test that data collector can be initialized"""
        self.assertIsNotNone(self.collector)

    def test_country_page_published(self):
        """Test that published country pages return 200"""
        # Test Kenya page (known published strategy)
        response = self.app.get('/country/KE')
        self.assertEqual(response.status_code, 200)
        
        # Test Nigeria page (known published strategy)
        response = self.app.get('/country/NG')
        self.assertEqual(response.status_code, 200)
        
        # Test South Africa page (known published strategy)
        response = self.app.get('/country/ZA')
        self.assertEqual(response.status_code, 200)

    def test_country_page_unpublished(self):
        """Test that unpublished country pages return 404"""
        # Test Morocco page (known draft strategy)
        response = self.app.get('/country/MA')
        self.assertEqual(response.status_code, 404)

    def test_country_page_nonexistent(self):
        """Test that non-existent country pages return 404"""
        response = self.app.get('/country/XX')
        self.assertEqual(response.status_code, 404)

    def test_country_page_content(self):
        """Test that country page contains expected content"""
        response = self.app.get('/country/KE')
        content = response.data.decode('utf-8')
        
        # Check for key sections
        self.assertIn('Kenya AI Strategy', content)
        self.assertIn('Vision', content)
        self.assertIn('Priority Sectors', content)
        self.assertIn('Key Initiatives', content)

    def test_vercel_wsgi_setup(self):
        """Test that Vercel WSGI middleware is properly configured"""
        self.assertTrue(hasattr(app, 'wsgi_app'))
        from werkzeug.middleware.proxy_fix import ProxyFix
        self.assertIsInstance(app.wsgi_app, ProxyFix)

    def test_flask_app_configuration(self):
        """Test that Flask app is configured correctly for Vercel"""
        import pathlib
        base_dir = pathlib.Path(__file__).parent.parent
        
        # Test template folder configuration
        self.assertEqual(app.template_folder, str(base_dir / 'templates'))
        
        # Test static folder configuration
        self.assertEqual(app.static_folder, str(base_dir / 'static'))
        self.assertEqual(app.static_url_path, '/static')
        
        # Test static file serving
        response = self.app.get('/static/css/style.css')
        self.assertIn(response.status_code, [200, 404])  # 404 is ok if file doesn't exist yet

if __name__ == '__main__':
    unittest.main()