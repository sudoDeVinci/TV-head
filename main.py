#!/usr/bin/env python3
"""
TV Head Main Application

This is the main entry point for the TV Head cosplay project.
It provides a command-line interface for configuring and running
the LED matrix display system.
"""

import sys
import argparse
import logging
from pathlib import Path
from typing import Optional

from controller import TVHeadController, ImageSettings
from tvlib._config import Config
from tvlib.comparator import convert_all, convert_dir
from tvlib.transformations import Rotation, Flip


def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('tvhead.log'),
        ]
    )


def configure_settings() -> Optional[ImageSettings]:
    """Run the interactive configuration interface."""
    controller = TVHeadController()
    settings = controller.run()
    
    if settings:
        logging.info(f"Configuration completed: {settings}")
        return settings
    else:
        logging.info("Configuration cancelled by user")
        return None


def convert_animations(settings: ImageSettings, target_dir: Optional[str] = None) -> bool:
    """Convert animation frames based on settings."""
    try:
        if not settings.resolution:
            logging.error("No resolution configured")
            return False
            
        if target_dir:
            logging.info(f"Converting animations in directory: {target_dir}")
            result = convert_dir(target_dir, settings.resolution, settings.rotation, settings.flip)
            success = result is not None
        else:
            logging.info("Converting all animations")
            success = convert_all(settings.resolution, settings.rotation, settings.flip)
        
        if success:
            logging.info("Animation conversion completed successfully")
        else:
            logging.error("Animation conversion failed")
            
        return success
        
    except Exception as e:
        logging.error(f"Error during animation conversion: {e}")
        return False


def main() -> int:
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description="TV Head LED Matrix Display Controller",
        epilog="For more information, see README.md"
    )
    
    parser.add_argument(
        "--configure", "-c",
        action="store_true",
        help="Run interactive configuration"
    )
    
    parser.add_argument(
        "--convert-all", "-a",
        action="store_true", 
        help="Convert all animations with current config"
    )
    
    parser.add_argument(
        "--convert-dir", "-d",
        metavar="DIR",
        help="Convert animations in specific directory"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--config-file",
        default="conf.toml",
        help="Configuration file path (default: conf.toml)"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    logging.info("TV Head application starting")
    
    # Load configuration
    if not Config.load():
        logging.error("Failed to load configuration")
        return 1
    
    settings = None
    
    # Handle configuration mode
    if args.configure:
        settings = configure_settings()
        if not settings:
            return 1
    
    # Handle conversion modes
    if args.convert_all or args.convert_dir:
        if not settings:
            # Use default settings if not configured interactively
            settings = ImageSettings()
            try:
                settings.resolution = Config.resolution()
            except ValueError as e:
                logging.error(f"Configuration error: {e}")
                return 1
        
        success = False
        if args.convert_all:
            success = convert_animations(settings)
        elif args.convert_dir:
            if not Path(f"animations/{args.convert_dir}").exists():
                logging.error(f"Directory not found: animations/{args.convert_dir}")
                return 1
            success = convert_animations(settings, args.convert_dir)
        
        if not success:
            return 1
    
    # If no specific action was requested, run configuration
    if not any([args.configure, args.convert_all, args.convert_dir]):
        settings = configure_settings()
        if not settings:
            return 1
        
        # Ask user if they want to convert animations
        try:
            response = input("\nWould you like to convert animations now? (y/N): ").strip().lower()
            if response in ['y', 'yes']:
                convert_animations(settings)
        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
            return 0
    
    logging.info("TV Head application completed successfully")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        sys.exit(1)