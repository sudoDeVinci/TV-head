# Contributing to TV Head 🤖

We love your input! We want to make contributing to TV Head as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## 🚀 Development Workflow

We use GitHub to host code, track issues and feature requests, and accept pull requests.

### Pull Requests Process

1. **Fork the repository** and create your branch from `main`
2. **Install development dependencies**: `pip install -e ".[dev]"`
3. **Make your changes** with comprehensive tests
4. **Ensure the test suite passes**: `python -m pytest`
5. **Format your code**: `black . && isort .`
6. **Type check**: `mypy .`
7. **Update documentation** as needed
8. **Issue a pull request**

### Branch Naming Convention

- `feature/description` - New features
- `bugfix/issue-number` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

## 🧪 Code Standards

### Style Guide

- **Formatter**: [Black](https://black.readthedocs.io/) with 88 character line length
- **Import sorting**: [isort](https://pycqa.github.io/isort/) 
- **Linting**: [flake8](https://flake8.pycqa.org/) with custom configuration
- **Type checking**: [mypy](https://mypy.readthedocs.io/) with strict mode

### Code Quality Requirements

- ✅ **Type annotations** on all public APIs
- ✅ **Docstrings** for all modules, classes, and functions
- ✅ **Test coverage** >90% for new code
- ✅ **Error handling** with appropriate logging
- ✅ **Performance considerations** for embedded targets

### Documentation Standards

```python
def process_animation(
    frames: List[ImageFrame], 
    target_resolution: Tuple[int, int],
    compression_level: float = 0.8
) -> AnimationData:
    """
    Process animation frames for microcontroller deployment.
    
    Args:
        frames: List of input image frames
        target_resolution: Output (width, height) in pixels
        compression_level: Differential compression ratio (0.0-1.0)
        
    Returns:
        Optimized animation data ready for JSON serialization
        
    Raises:
        ValueError: If compression_level is out of range
        ProcessingError: If frame processing fails
        
    Example:
        >>> frames = load_frames("animation/smile/")
        >>> data = process_animation(frames, (16, 16), 0.9)
        >>> save_json(data, "output/smile.json")
    """
```

## 🧪 Testing

### Test Structure

```
tests/
├── unit/           # Unit tests for individual components
├── integration/    # Integration tests for full workflows  
├── hardware/       # Hardware-in-the-loop tests
├── performance/    # Benchmarking and profiling
└── fixtures/       # Test data and mock objects
```

### Writing Tests

```python
import pytest
from tvlib.comparator import convert_images
from tests.fixtures import sample_images, mock_config

class TestImageConverter:
    """Test suite for image conversion functionality."""
    
    @pytest.fixture
    def sample_frames(self):
        """Provide sample animation frames for testing."""
        return sample_images.load_test_animation()
    
    def test_differential_compression(self, sample_frames):
        """Test that differential compression reduces file size."""
        result = convert_images(
            sample_frames, 
            target_dimensions=(16, 16),
            compression=True
        )
        
        assert result is not None
        assert len(result.frames) == len(sample_frames)
        assert result.compression_ratio > 0.5
    
    @pytest.mark.parametrize("resolution", [(8, 8), (16, 16), (32, 32)])
    def test_multiple_resolutions(self, sample_frames, resolution):
        """Test conversion works across different resolutions."""
        result = convert_images(sample_frames, target_dimensions=resolution)
        assert result.metadata.width == resolution[0]
        assert result.metadata.height == resolution[1]
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=tvlib --cov-report=html

# Run specific test category
python -m pytest tests/unit/

# Run performance benchmarks
python -m pytest tests/performance/ --benchmark-only

# Run hardware tests (requires connected device)
python -m pytest tests/hardware/ --hardware-connected
```

## 🎯 Feature Development

### New Feature Checklist

- [ ] **Design document** in `docs/rfcs/` (for major features)
- [ ] **Implementation** with type annotations
- [ ] **Unit tests** with >90% coverage  
- [ ] **Integration tests** for end-to-end workflows
- [ ] **Performance benchmarks** if applicable
- [ ] **Documentation updates** in relevant files
- [ ] **Example usage** in docstrings or examples/
- [ ] **Microcontroller compatibility** testing

### Performance Considerations

Since TV Head targets resource-constrained microcontrollers:

- **Memory efficiency**: Prefer generators over lists for large datasets
- **File size optimization**: Minimize JSON output size
- **Processing speed**: Profile critical paths with `cProfile`
- **Hardware compatibility**: Test on actual target devices when possible

## 🐛 Bug Reports

Great bug reports include:

1. **Environment details**:
   - Python version
   - Operating system
   - Hardware platform (if applicable)
   - Package versions (`pip freeze`)

2. **Reproduction steps**:
   - Minimal code example
   - Input data (or sample that reproduces issue)
   - Expected vs actual behavior

3. **Error information**:
   - Full traceback
   - Log output with debug level
   - Screenshots/videos if UI-related

### Bug Report Template

```markdown
**Environment:**
- Python: 3.9.7
- OS: Ubuntu 20.04
- Hardware: ESP32-S3

**Description:**
Brief description of the issue

**Steps to Reproduce:**
1. Run command X
2. Load file Y  
3. Observe error Z

**Expected Behavior:**
What you expected to happen

**Actual Behavior:**
What actually happened

**Error Output:**
```
Paste full traceback here
```

**Additional Context:**
Any other relevant information
```

## 📋 Project Areas

### Good First Issues

- Documentation improvements
- Adding type annotations
- Writing tests for existing code
- Performance optimizations
- Hardware platform support

### Advanced Contributions

- New compression algorithms
- Real-time streaming protocols
- Hardware abstraction layers
- Web-based animation editors
- Machine learning integration

## 🏗️ Architecture Guidelines

### Module Organization

```
tvlib/
├── core/           # Core algorithms and data structures
├── hardware/       # Hardware abstraction and drivers  
├── formats/        # File format handlers (JSON, etc.)
├── transforms/     # Image transformation pipeline
├── compression/    # Compression algorithms
└── utils/          # Utility functions and helpers
```

### Dependency Management

- **Core dependencies**: Minimize for embedded compatibility
- **Optional dependencies**: Use graceful degradation
- **Development dependencies**: Separate from runtime requirements

### API Design Principles

- **Consistency**: Similar functions should have similar signatures
- **Discoverability**: Clear naming and comprehensive docstrings
- **Flexibility**: Support common use cases with sensible defaults
- **Performance**: Optimize hot paths, profile before optimizing

## 🔐 Security

### Reporting Security Issues

**DO NOT** report security vulnerabilities through public GitHub issues.

Instead, email `tadj.d.cazaubon@gmail.com` with:
- Description of the vulnerability
- Steps to reproduce
- Potential impact assessment
- Suggested fix (if known)

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙋‍♀️ Questions?

- 💬 **General questions**: [GitHub Discussions](https://github.com/sudoDeVinci/TV-head/discussions)
- 🐛 **Bug reports**: [GitHub Issues](https://github.com/sudoDeVinci/TV-head/issues)
- 📧 **Direct contact**: tadj.d.cazaubon@gmail.com

---

Thanks for contributing to TV Head! 🎉
