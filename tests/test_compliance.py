#!/usr/bin/env python3
"""
Compliance testing for Claude Specifications Repository.
Tests markdown formatting, required sections, and calculates compliance percentage.
"""

import os
import re
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple


class SpecificationTester:
    """Test specifications for compliance with repository standards."""
    
    REQUIRED_SECTIONS = [
        "SYSTEM OVERVIEW",
        "ROLE DEFINITION", 
        "OPERATING INSTRUCTIONS",
        "FUNCTIONAL REQUIREMENTS",
        "INTEGRATION DETAILS",  # Optional - only required if external systems mentioned
        "WORKFLOWS & PROTOCOLS",
        "RESPONSE PATTERNS & EXAMPLES",
        "QUALITY STANDARDS",
        "VERSION HISTORY"
    ]
    
    REQUIRED_SUBSECTIONS = {
        "SYSTEM OVERVIEW": ["Name:", "Version:", "Purpose:", "Category:"],
        "OPERATING INSTRUCTIONS": ["Command Structure", "Core Principles"],
        "FUNCTIONAL REQUIREMENTS": ["Primary Functions", "Constraints", "Success Criteria"],
        "QUALITY STANDARDS": ["Performance Metrics", "Accuracy Requirements", "User Experience Criteria"],
        "VERSION HISTORY": ["v"]
    }
    
    VALID_CATEGORIES = ["productivity", "coding", "communication", "research", "creative"]
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.results = []
        
    def test_all_specifications(self) -> Tuple[bool, List[Dict]]:
        """Test all specification files in the repository."""
        all_passed = True
        
        # Find all .md files in category directories
        for category in self.VALID_CATEGORIES:
            category_path = self.repo_root / category
            if category_path.exists():
                for spec_file in category_path.glob("*.md"):
                    # Skip README files
                    if spec_file.name.lower() == "readme.md":
                        continue
                        
                    result = self.test_specification(spec_file)
                    self.results.append(result)
                    
                    if result["compliance_percentage"] < 90:
                        all_passed = False
                        
        return all_passed, self.results
    
    def test_specification(self, spec_path: Path) -> Dict:
        """Test a single specification file."""
        print(f"\nTesting: {spec_path}")
        
        result = {
            "file": str(spec_path.relative_to(self.repo_root)),
            "errors": [],
            "warnings": [],
            "compliance_percentage": 0,
            "sections_found": [],
            "sections_missing": []
        }
        
        # Read file content
        try:
            with open(spec_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            result["errors"].append(f"Failed to read file: {e}")
            return result
            
        # Test 1: Check markdown formatting
        if not self._check_markdown_format(content, result):
            result["errors"].append("Invalid markdown formatting")
            
        # Test 2: Check file location
        if not self._check_file_location(spec_path, result):
            result["errors"].append("Invalid file location")
            
        # Test 3: Check required sections
        sections_score = self._check_required_sections(content, result)
        
        # Test 4: Check section content
        content_score = self._check_section_content(content, result)
        
        # Calculate compliance percentage
        total_score = sections_score + content_score
        result["compliance_percentage"] = total_score
        
        # Print results
        self._print_result(result)
        
        return result
    
    def _check_markdown_format(self, content: str, result: Dict) -> bool:
        """Check basic markdown formatting."""
        issues = []
        
        # Check for title
        if not content.strip().startswith("#"):
            issues.append("Missing top-level title")
            
        # Check for proper header hierarchy
        lines = content.split('\n')
        header_levels = []
        for line in lines:
            if line.strip().startswith('#') and not line.strip().startswith('#####'):  # Ignore 5+ level headers
                # Count the number of # at the start
                match = re.match(r'^(#+)\s', line.strip())
                if match:
                    level = len(match.group(1))
                    if level <= 4:  # Only track up to #### headers
                        header_levels.append(level)
                
        # Check if headers skip levels (more lenient)
        prev_level = 0
        for level in header_levels:
            if level > prev_level + 2:  # Allow skipping one level
                issues.append("Header hierarchy skips multiple levels")
                break
            prev_level = level
                
        if issues:
            result["errors"].extend(issues)
            return False
        return True
    
    def _check_file_location(self, spec_path: Path, result: Dict) -> bool:
        """Check if file is in correct location."""
        parent_dir = spec_path.parent.name
        
        if parent_dir not in self.VALID_CATEGORIES:
            result["errors"].append(f"File not in valid category directory. Found in: {parent_dir}")
            return False
        return True
    
    def _check_required_sections(self, content: str, result: Dict) -> int:
        """Check for required sections and return score."""
        score = 0
        max_score = 50  # 50% of total score
        
        # Find all section headers
        section_pattern = r'^##\s+([A-Z\s&]+)$'
        found_sections = re.findall(section_pattern, content, re.MULTILINE)
        found_sections = [s.strip() for s in found_sections]
        
        # Check each required section
        for section in self.REQUIRED_SECTIONS:
            if section in found_sections:
                result["sections_found"].append(section)
                # Special case: INTEGRATION DETAILS is optional
                if section == "INTEGRATION DETAILS":
                    # Check if external systems are mentioned
                    if "external" in content.lower() or "integration" in content.lower():
                        score += max_score / len(self.REQUIRED_SECTIONS)
                else:
                    score += max_score / len(self.REQUIRED_SECTIONS)
            else:
                # INTEGRATION DETAILS is optional if no external systems
                if section == "INTEGRATION DETAILS":
                    if "external" not in content.lower() and "integration" not in content.lower():
                        score += max_score / len(self.REQUIRED_SECTIONS)
                        result["sections_found"].append(f"{section} (not required)")
                    else:
                        result["sections_missing"].append(section)
                else:
                    result["sections_missing"].append(section)
                    
        return int(score)
    
    def _check_section_content(self, content: str, result: Dict) -> int:
        """Check section content and return score."""
        score = 0
        max_score = 50  # 50% of total score
        points_per_check = max_score / 5  # 5 content checks
        
        # Check 1: SYSTEM OVERVIEW content
        if "## SYSTEM OVERVIEW" in content:
            section_content = self._extract_section_content(content, "SYSTEM OVERVIEW")
            required = ["Name:", "Version:", "Purpose:", "Category:"]
            if all(req in section_content for req in required):
                score += points_per_check
            else:
                missing = [req for req in required if req not in section_content]
                result["warnings"].append(f"SYSTEM OVERVIEW missing: {', '.join(missing)}")
                
        # Check 2: RESPONSE PATTERNS has at least 2 examples
        if "## RESPONSE PATTERNS & EXAMPLES" in content:
            section_content = self._extract_section_content(content, "RESPONSE PATTERNS & EXAMPLES")
            # Count patterns more flexibly - look for ### Pattern followed by optional number/name and colon
            pattern_matches = re.findall(r'###\s+Pattern\s*[\w\s]*:', section_content)
            pattern_count = len(pattern_matches)
            if pattern_count >= 2:
                score += points_per_check
            else:
                result["warnings"].append(f"RESPONSE PATTERNS needs at least 2 examples (found {pattern_count})")
                
        # Check 3: QUALITY STANDARDS has all subsections
        if "## QUALITY STANDARDS" in content:
            section_content = self._extract_section_content(content, "QUALITY STANDARDS")
            required = ["Performance Metrics", "Accuracy Requirements", "User Experience Criteria"]
            # Check more flexibly - with or without ### prefix
            found_all = True
            missing = []
            for req in required:
                if req not in section_content and f"### {req}" not in section_content:
                    found_all = False
                    missing.append(req)
            
            if found_all:
                score += points_per_check
            else:
                result["warnings"].append(f"QUALITY STANDARDS missing: {', '.join(missing)}")
                
        # Check 4: VERSION HISTORY has version with date
        if "## VERSION HISTORY" in content:
            section_content = self._extract_section_content(content, "VERSION HISTORY")
            if re.search(r'v\d+\.\d+.*\[\d{4}-\d{2}-\d{2}\]', section_content):
                score += points_per_check
            else:
                result["warnings"].append("VERSION HISTORY needs version number and date in format [YYYY-MM-DD]")
                
        # Check 5: General content quality
        if len(content) > 1000 and content.count('##') >= 5:
            score += points_per_check
        else:
            result["warnings"].append("Specification seems too brief or lacking detail")
            
        return int(score)
    
    def _extract_section_content(self, content: str, section_name: str) -> str:
        """Extract content of a specific section."""
        # Find the section header
        section_start = content.find(f"## {section_name}")
        if section_start == -1:
            return ""
        
        # Find the next section header (## followed by capital letters, not in code blocks)
        # Look for ## at the start of a line (after newline)
        remaining_content = content[section_start + len(f"## {section_name}"):]
        next_section_match = None
        
        # Split by lines and track if we're in a code block
        lines = remaining_content.split('\n')
        in_code_block = False
        for i, line in enumerate(lines):
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
            elif not in_code_block and re.match(r'^##\s+[A-Z][A-Z\s&]+$', line.strip()):
                next_section_match = i
                break
        
        if next_section_match is not None:
            # Count characters up to the match
            section_end = section_start + len(f"## {section_name}") + sum(len(lines[j]) + 1 for j in range(next_section_match))
        else:
            section_end = len(content)
            
        return content[section_start:section_end]
    
    def _print_result(self, result: Dict) -> None:
        """Print test result for a specification."""
        print(f"  Compliance: {result['compliance_percentage']}%")
        
        if result["errors"]:
            print("  ❌ Errors:")
            for error in result["errors"]:
                print(f"     - {error}")
                
        if result["warnings"]:
            print("  ⚠️  Warnings:")
            for warning in result["warnings"]:
                print(f"     - {warning}")
                
        if result["sections_missing"]:
            print("  📋 Missing sections:")
            for section in result["sections_missing"]:
                print(f"     - {section}")
                
        if result["compliance_percentage"] >= 90:
            print("  ✅ PASSED")
        else:
            print("  ❌ FAILED (minimum 90% required)")


def main():
    """Main test runner."""
    # Get repository root
    repo_root = Path(__file__).parent.parent
    
    print("🧪 Claude Specifications Compliance Test")
    print("=" * 50)
    
    # Run tests
    tester = SpecificationTester(repo_root)
    all_passed, results = tester.test_all_specifications()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    
    total_specs = len(results)
    passed_specs = sum(1 for r in results if r["compliance_percentage"] >= 90)
    failed_specs = total_specs - passed_specs
    
    print(f"Total specifications tested: {total_specs}")
    print(f"Passed (≥90% compliance): {passed_specs}")
    print(f"Failed (<90% compliance): {failed_specs}")
    
    if failed_specs > 0:
        print("\n❌ Failed specifications:")
        for result in results:
            if result["compliance_percentage"] < 90:
                print(f"   - {result['file']}: {result['compliance_percentage']}%")
    
    # Write results to JSON for CI/CD
    results_file = repo_root / "test_results.json"
    with open(results_file, 'w') as f:
        json.dump({
            "all_passed": all_passed,
            "total_specs": total_specs,
            "passed_specs": passed_specs,
            "failed_specs": failed_specs,
            "results": results
        }, f, indent=2)
    
    print(f"\nDetailed results written to: {results_file}")
    
    # Exit with appropriate code
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()