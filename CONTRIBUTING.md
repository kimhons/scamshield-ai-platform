# Contributing to ScamShield AI

Thank you for your interest in contributing to ScamShield AI! This document provides guidelines and information for contributors.

## 🤝 Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please read and follow our Code of Conduct.

### Our Standards

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Git
- Basic understanding of AI/ML concepts
- Familiarity with Flask and React

### Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/scamshield-ai-platform.git
   cd scamshield-ai-platform
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Set up the frontend**
   ```bash
   cd ../frontend
   npm install
   ```

4. **Configure environment variables**
   ```bash
   cp backend/.env.example backend/.env
   # Edit .env with your configuration
   ```

## 📝 Development Guidelines

### Code Style

**Python (Backend)**
- Follow PEP 8 style guidelines
- Use Black for code formatting: `black src/`
- Use flake8 for linting: `flake8 src/`
- Maximum line length: 88 characters
- Use type hints for all functions

**JavaScript/TypeScript (Frontend)**
- Follow ESLint configuration
- Use Prettier for formatting: `npm run format`
- Use meaningful variable and function names
- Prefer functional components with hooks

### Commit Messages

Use conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(ai-engine): add DeepSeek model integration
fix(frontend): resolve investigation status polling issue
docs(readme): update installation instructions
```

### Testing

**Backend Testing**
```bash
cd backend
pytest tests/ -v --cov=src
```

**Frontend Testing**
```bash
cd frontend
npm test
npm run test:coverage
```

**Requirements:**
- Minimum 90% code coverage for new features
- All tests must pass before submitting PR
- Include both unit and integration tests

### Documentation

- Update README.md for significant changes
- Add docstrings to all Python functions
- Include JSDoc comments for complex JavaScript functions
- Update API documentation for new endpoints

## 🔧 Contributing Process

### 1. Choose an Issue

- Check existing issues for something to work on
- Look for issues labeled `good first issue` for beginners
- Comment on the issue to indicate you're working on it

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 3. Make Changes

- Write clean, well-documented code
- Follow the coding standards
- Add tests for new functionality
- Update documentation as needed

### 4. Test Your Changes

```bash
# Backend tests
cd backend
pytest tests/ -v

# Frontend tests
cd frontend
npm test

# Integration tests
npm run test:integration
```

### 5. Submit a Pull Request

1. **Push your branch**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request**
   - Use a clear, descriptive title
   - Include a detailed description of changes
   - Reference any related issues
   - Add screenshots for UI changes

3. **PR Template**
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update

   ## Testing
   - [ ] Tests pass locally
   - [ ] Added new tests for functionality
   - [ ] Updated documentation

   ## Screenshots (if applicable)
   
   ## Related Issues
   Closes #123
   ```

## 🏗️ Architecture Guidelines

### Backend Structure

```
backend/
├── src/
│   ├── ai_engine/          # AI model management
│   ├── models/             # Database models
│   ├── routes/             # API endpoints
│   ├── utils/              # Utility functions
│   └── main.py             # Application entry point
├── tests/                  # Test files
└── requirements.txt        # Dependencies
```

### Frontend Structure

```
frontend/
├── src/
│   ├── components/         # React components
│   ├── hooks/              # Custom hooks
│   ├── lib/                # Utility functions
│   ├── pages/              # Page components
│   └── types/              # TypeScript types
├── public/                 # Static assets
└── package.json            # Dependencies
```

### AI Engine Guidelines

When contributing to the AI engine:

1. **Model Integration**
   - Add new models to `model_manager_v2.py`
   - Include proper error handling and fallbacks
   - Add cost tracking and optimization

2. **Investigation Engine**
   - Maintain tier-based processing logic
   - Ensure proper artifact validation
   - Include comprehensive logging

3. **Intelligence Fusion**
   - Add new threat correlation methods
   - Maintain attribution analysis accuracy
   - Include pattern recognition improvements

## 🐛 Bug Reports

### Before Submitting

1. Check existing issues for duplicates
2. Test with the latest version
3. Gather relevant information

### Bug Report Template

```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Windows 10, macOS 12]
- Browser: [e.g., Chrome 96]
- Python Version: [e.g., 3.11.0]
- Node Version: [e.g., 18.0.0]

**Additional Context**
Screenshots, logs, etc.
```

## 💡 Feature Requests

### Before Submitting

1. Check if the feature already exists
2. Consider if it fits the project scope
3. Think about implementation complexity

### Feature Request Template

```markdown
**Feature Description**
Clear description of the proposed feature

**Use Case**
Why is this feature needed?

**Proposed Solution**
How should this feature work?

**Alternatives Considered**
Other approaches you've considered

**Additional Context**
Mockups, examples, etc.
```

## 🏷️ Labels

We use labels to categorize issues and PRs:

**Type Labels:**
- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Documentation improvements
- `question`: Further information is requested

**Priority Labels:**
- `priority: high`: Critical issues
- `priority: medium`: Important improvements
- `priority: low`: Nice to have features

**Difficulty Labels:**
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `advanced`: Requires deep knowledge

## 🎯 Areas for Contribution

### High Priority Areas

1. **AI Model Integration**
   - New model providers
   - Performance optimization
   - Cost reduction strategies

2. **Investigation Capabilities**
   - New artifact types
   - Enhanced analysis methods
   - Improved accuracy

3. **User Experience**
   - UI/UX improvements
   - Performance optimization
   - Accessibility features

4. **Security & Compliance**
   - Security enhancements
   - Compliance frameworks
   - Audit capabilities

### Documentation Needs

- API documentation
- Deployment guides
- Tutorial content
- Architecture documentation

### Testing Improvements

- Unit test coverage
- Integration tests
- Performance tests
- Security tests

## 🏆 Recognition

Contributors will be recognized in:

- README.md contributors section
- Release notes for significant contributions
- Annual contributor highlights
- Special badges for major contributions

## 📞 Getting Help

If you need help:

1. **Discord**: Join our [community Discord](https://discord.gg/scamshield-ai)
2. **Email**: contributors@scamshield.ai
3. **Issues**: Create a question issue
4. **Discussions**: Use GitHub Discussions for general questions

## 📄 License

By contributing to ScamShield AI, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to ScamShield AI! Together, we're building the future of fraud prevention. 🛡️

