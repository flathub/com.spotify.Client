"""Shared pytest fixtures for testing."""

import tempfile
import shutil
import json
from pathlib import Path
from unittest.mock import Mock, MagicMock
import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def mock_requests():
    """Mock requests module for HTTP calls."""
    mock_requests = Mock()
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"test": "data"}
    mock_response.text = "test response"
    mock_response.iter_content.return_value = [b"test chunk"]
    mock_requests.get.return_value = mock_response
    return mock_requests


@pytest.fixture
def sample_snap_info():
    """Sample snap info data for testing."""
    return {
        "channel-map": [
            {
                "channel": {
                    "risk": "stable",
                    "released-at": "2024-01-01T00:00:00Z"
                },
                "download": {
                    "sha3-384": "test-sha3-384",
                    "url": "https://example.com/test.snap",
                    "size": 123456789
                },
                "version": "1.2.3.456"
            }
        ]
    }


@pytest.fixture
def sample_manifest_data():
    """Sample manifest JSON data for testing."""
    return {
        "modules": [
            {
                "name": "spotify",
                "sources": [
                    {
                        "type": "extra-data",
                        "url": "https://old-url.com/test.snap",
                        "sha256": "old-sha256",
                        "size": 987654321
                    }
                ]
            }
        ]
    }


@pytest.fixture
def mock_manifest_file(temp_dir, sample_manifest_data):
    """Create a mock manifest file."""
    manifest_path = temp_dir / "com.spotify.Client.json"
    with open(manifest_path, "w") as f:
        json.dump(sample_manifest_data, f, indent=4)
    return manifest_path


@pytest.fixture
def sample_appdata_xml():
    """Sample appdata XML content."""
    return """<?xml version='1.0' encoding='utf-8'?>
<component>
  <id>com.spotify.Client</id>
  <name>Spotify</name>
  <releases>
  </releases>
</component>"""


@pytest.fixture
def mock_appdata_file(temp_dir, sample_appdata_xml):
    """Create a mock appdata XML file."""
    appdata_path = temp_dir / "com.spotify.Client.appdata.xml"
    with open(appdata_path, "w") as f:
        f.write(sample_appdata_xml)
    return appdata_path


@pytest.fixture
def mock_xsettings():
    """Mock XSettings data."""
    return {
        b'Gdk/WindowScalingFactor': 2.0,
        b'Net/ThemeName': b'Adwaita',
        b'Gtk/FontName': b'Cantarell 11'
    }


@pytest.fixture
def mock_env_vars():
    """Mock environment variables."""
    return {
        'GDK_SCALE': '1.5',
        'DISPLAY': ':0'
    }


@pytest.fixture
def mock_xcb_library():
    """Mock XCB library for testing XSettings functionality."""
    mock_xcb = MagicMock()
    mock_connection = MagicMock()
    
    # Mock XCB connection
    mock_xcb.xcb_connect.return_value = mock_connection
    mock_xcb.xcb_connection_has_error.return_value = 0
    
    # Mock cookie and reply structures
    mock_cookie = MagicMock()
    mock_reply = MagicMock()
    mock_reply.contents.payload = 12345  # Mock atom ID
    
    mock_xcb.xcb_intern_atom.return_value = mock_cookie
    mock_xcb.xcb_intern_atom_reply.return_value = mock_reply
    mock_xcb.xcb_get_selection_owner.return_value = mock_cookie
    mock_xcb.xcb_get_selection_owner_reply.return_value = mock_reply
    mock_xcb.xcb_get_property.return_value = mock_cookie
    
    # Mock property reply with sample XSettings data
    sample_data = b'\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00'  # Minimal XSettings
    mock_property_reply = MagicMock()
    mock_xcb.xcb_get_property_reply.return_value = mock_property_reply
    mock_xcb.xcb_get_property_value_length.return_value = len(sample_data)
    mock_xcb.xcb_get_property_value.return_value = sample_data
    
    return mock_xcb


@pytest.fixture(autouse=True)
def reset_mocks():
    """Reset all mocks after each test."""
    yield
    # This fixture runs after each test to ensure clean state