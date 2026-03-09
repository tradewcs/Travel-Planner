import pytest
from datetime import date

from app.db.models import Project, ProjectStatus


class TestProjectModel:
    def test_create_project(self):
        project = Project(
            name="Test Project",
            description="Test Description",
            start_date=date.today()
        )
        
        assert project.name == "Test Project"
        assert project.description == "Test Description"
        assert project.start_date == date.today()
        assert project.status == ProjectStatus.ACTIVE
        assert project.places_count == 0
        assert project.is_completed is False
    
    def test_can_add_place_when_under_limit(self):
        project = Project(name="Test")
        assert project.can_add_place() is True
    
    def test_cannot_add_place_when_at_limit(self, mocker):
        project = Project(name="Test")
        project.project_places = [mocker.Mock() for _ in range(10)]
        assert project.can_add_place() is False
    
    def test_project_completed_when_all_places_visited(self, mocker):
        project = Project(name="Test")
        place1 = mocker.Mock(visited=True)
        place2 = mocker.Mock(visited=True)
        project.project_places = [place1, place2]
        
        assert project.is_completed is True
    
    def test_project_not_completed_when_some_places_not_visited(self, mocker):
        project = Project(name="Test")
        place1 = mocker.Mock(visited=True)
        place2 = mocker.Mock(visited=False)
        project.project_places = [place1, place2]
        
        assert project.is_completed is False