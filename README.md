# Claude Specifications Repository

This repository contains a collection of specifications for Claude AI systems, organized by category for easy navigation and reference.

## Repository Structure

```
claude-specs/
├── README.md                    # This file
├── TEMPLATE.md                  # Template for new specifications
├── productivity/                # Productivity & workflow specs
├── coding/                      # Programming & development specs
├── communication/               # Communication & interaction specs
├── research/                    # Research & analysis specs
└── creative/                    # Creative work specs
```

## Categories

### [Productivity](./productivity/)
Specifications for productivity tools, workflow automation, and task management systems.
- [GTD Expert System](./productivity/gtd-expert-system.md) - David Allen GTD implementation with Notion integration

### [Coding](./coding/)
Specifications for programming assistants, code generation, and development tools.
- [AI Prompt Generator](./coding/ai-prompt-generator.md) - Advanced prompt engineering system
- [iOS App Prototype Assistant](./coding/ios-app-prototype-assistant.md) - Rapid iOS prototyping with business strategy

### [Communication](./communication/)
Specifications for communication styles, interaction patterns, and conversational agents.
- [SaborConFlow Social Media](./communication/saborconflow-social-media.md) - Social media strategy for Latin dance school

### [Research](./research/)
Specifications for research assistants, analysis tools, and information synthesis.

### [Creative](./creative/)
Specifications for creative writing, design, and artistic collaboration.

## Adding New Specifications

1. Choose the appropriate category folder
2. Copy the [TEMPLATE.md](./TEMPLATE.md) file
3. Follow the template structure for consistency
4. Update this README with a link to your new specification

## Specification Format

All specifications should include:
- System overview and version
- Role definition or purpose
- Operating instructions
- Core principles or requirements
- Implementation details
- Examples or patterns

See [TEMPLATE.md](./TEMPLATE.md) for the standard format.

## Quality Standards & Compliance

All specifications must achieve **90% minimum compliance** with the repository template. This is enforced through automated CI/CD testing.

### Automated Testing

Every pull request triggers:
- **Compliance Check** - Validates template structure and content
- **Markdown Linting** - Ensures consistent formatting
- **Directory Structure** - Verifies correct file placement

### Running Tests Locally

```bash
# Run all compliance tests
python tests/test_compliance.py

# Test a specific specification
python -c "from pathlib import Path; from tests.test_compliance import SpecificationTester; tester = SpecificationTester(Path('.')); tester.test_specification(Path('path/to/spec.md'))"
```

## Contributing

When adding new specifications:
1. Use [TEMPLATE.md](./TEMPLATE.md) as your starting point
2. Ensure 90% compliance before submitting PR
3. Place files in correct category directory
4. Update category README with description
5. Add link to this main README
6. Run compliance tests locally first
7. Address all CI/CD feedback in PR

### Branch Protection

The `main` branch is protected and requires:
- All CI/CD checks passing
- At least one approval
- No merge conflicts

See [Branch Protection Setup](./.github/BRANCH_PROTECTION.md) for details.

## Quick Links

- [Specification Template](./TEMPLATE.md)
- [GTD Expert System](./productivity/gtd-expert-system.md)
- [AI Prompt Generator](./coding/ai-prompt-generator.md)
- [iOS App Prototype Assistant](./coding/ios-app-prototype-assistant.md)
- [SaborConFlow Social Media](./communication/saborconflow-social-media.md)
