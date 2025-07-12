#!/usr/bin/env python3
"""
Test script to verify TV Head functionality.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported successfully."""
    print("Testing imports...")
    
    try:
        from tvlib import Config, Rotation, Flip
        print("✓ tvlib imports successful")
    except Exception as e:
        print(f"✗ tvlib import failed: {e}")
        return False
    
    try:
        from controller import TVHeadController, ImageSettings
        print("✓ controller imports successful")
    except Exception as e:
        print(f"✗ controller import failed: {e}")
        return False
    
    try:
        import ui
        print("✓ ui imports successful")
    except Exception as e:
        print(f"✗ ui import failed: {e}")
        return False
    
    return True

def test_config():
    """Test configuration loading."""
    print("\nTesting configuration...")
    
    try:
        from tvlib import Config
        
        # Test if config file exists
        if not os.path.exists("conf.toml"):
            print("✗ conf.toml not found")
            return False
        
        # Test config loading
        success = Config.load()
        if success:
            print("✓ Configuration loaded successfully")
            resolution = Config.resolution()
            print(f"✓ Resolution: {resolution}")
            board = Config.boardtype()
            print(f"✓ Board type: {board}")
            return True
        else:
            print("✗ Configuration loading failed")
            return False
            
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def test_transformations():
    """Test transformation enums."""
    print("\nTesting transformations...")
    
    try:
        from tvlib import Rotation, Flip
        
        # Test rotation enum
        rot = Rotation.ROTATE_90
        print(f"✓ Rotation enum works: {rot}")
        
        # Test flip enum
        flip = Flip.VERTICAL_FLIP
        print(f"✓ Flip enum works: {flip}")
        
        return True
        
    except Exception as e:
        print(f"✗ Transformation test failed: {e}")
        return False

def test_controller():
    """Test controller functionality."""
    print("\nTesting controller...")
    
    try:
        from controller import TVHeadController, ImageSettings
        
        # Test ImageSettings dataclass
        settings = ImageSettings()
        print(f"✓ ImageSettings created: {settings}")
        
        # Test controller creation
        controller = TVHeadController()
        print("✓ TVHeadController created successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Controller test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 50)
    print("TV HEAD PROJECT VERIFICATION")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_config,
        test_transformations, 
        test_controller,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} crashed: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 50)
    
    if failed == 0:
        print("🎉 All tests passed! The project is ready to use.")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
