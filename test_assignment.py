import unittest
import json
import os
import folium
import pandas as pd
from geopy.distance import geodesic
from bs4 import BeautifulSoup

class TestMappingAssignment(unittest.TestCase):
    def setUp(self):
        # Define the correct coordinates
        self.point1 = (36.325735, 43.928414)
        self.point2 = (36.393432, 44.586781)
        self.point3 = (36.660477, 43.840174)
        
        # Calculate correct distances
        self.correct_distances = {
            'p1_p2': round(geodesic(self.point1, self.point2).kilometers, 2),
            'p2_p3': round(geodesic(self.point2, self.point3).kilometers, 2),
            'p1_p3': round(geodesic(self.point1, self.point3).kilometers, 2)
        }
        
        self.total_points = 0

    def test_python_script(self, filename='solution.py'):
        """Test the Python script (30 points)"""
        points = 0
        try:
            # Check if file exists
            self.assertTrue(os.path.exists(filename), "Python script not found")
            points += 10

            # Check if required libraries are imported
            with open(filename, 'r') as f:
                content = f.read()
                self.assertIn('import folium', content, "folium import missing")
                self.assertIn('import geopy', content, "geopy import missing")
                points += 10

            # Check if script runs without errors
            exec(content, {}, {})
            points += 10

        except Exception as e:
            print(f"Error in Python script: {str(e)}")
        
        self.total_points += points
        return points

    def test_html_map(self, filename='map.html'):
        """Test the HTML map output (35 points)"""
        points = 0
        try:
            # Check if file exists
            self.assertTrue(os.path.exists(filename), "Map HTML file not found")
            points += 5

            # Parse HTML and check for markers
            with open(filename, 'r') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                
                # Check if it's a folium map
                self.assertTrue(soup.find('div', class_='folium-map'), "No folium map found")
                points += 10

                # Check for markers (looking in JavaScript code)
                script_content = str(soup.find_all('script'))
                
                # Check if all three points are present (approximately)
                coordinates = [
                    str(self.point1[0])[:5],
                    str(self.point1[1])[:5],
                    str(self.point2[0])[:5],
                    str(self.point2[1])[:5],
                    str(self.point3[0])[:5],
                    str(self.point3[1])[:5]
                ]
                
                for coord in coordinates:
                    self.assertIn(coord, script_content, f"Coordinate {coord} not found in map")
                    points += 5  # 5 points for each correct coordinate (30 total)

        except Exception as e:
            print(f"Error in HTML map: {str(e)}")
        
        self.total_points += points
        return points

    def test_distance_calculations(self, filename='distances.txt'):
        """Test the distance calculations (35 points)"""
        points = 0
        try:
            # Check if file exists
            self.assertTrue(os.path.exists(filename), "Distance calculations file not found")
            points += 5

            # Read and parse distances
            with open(filename, 'r') as f:
                content = f.read()
                
                # Extract numbers from text (assuming they're in km)
                import re
                numbers = [float(x) for x in re.findall(r"[\d.]+", content)]
                
                # Allow for small differences in calculation (0.1 km tolerance)
                correct_distances = list(self.correct_distances.values())
                for i, distance in enumerate(numbers):
                    self.assertAlmostEqual(distance, correct_distances[i], delta=0.1,
                                         msg=f"Distance calculation {i+1} is incorrect")
                    points += 10  # 10 points for each correct distance (30 total)

        except Exception as e:
            print(f"Error in distance calculations: {str(e)}")
        
        self.total_points += points
        return points

def grade_assignment():
    """Run all tests and return the total grade"""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMappingAssignment)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Get the test instance to access total_points
    test_instance = TestMappingAssignment()
    test_instance.setUp()
    
    # Run individual components
    python_points = test_instance.test_python_script()
    html_points = test_instance.test_html_map()
    distance_points = test_instance.test_distance_calculations()
    
    # Create detailed feedback
    feedback = {
        "total_score": test_instance.total_points,
        "python_script_score": python_points,
        "html_map_score": html_points,
        "distance_calculations_score": distance_points,
        "tests_passed": len(result.failures) == 0,
        "feedback": "All tests passed!" if len(result.failures) == 0 else str(result.failures)
    }
    
    # Write feedback to file
    with open('grading_results.json', 'w') as f:
        json.dump(feedback, f, indent=2)
    
    return test_instance.total_points

if __name__ == '__main__':
    grade_assignment()
