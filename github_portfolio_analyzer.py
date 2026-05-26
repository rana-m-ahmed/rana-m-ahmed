#!/usr/bin/env python3
"""
GitHub Portfolio Analyzer
Comprehensive analysis tool for GitHub repositories with detailed metrics for portfolio assessment.

Usage:
    python github_portfolio_analyzer.py [--token YOUR_TOKEN]

Environment Variables:
    GITHUB_TOKEN: Personal access token (classic) with 'repo' scope
"""

import os
import json
import sys
import re
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Optional, Tuple, Any
import urllib.request
import urllib.error
from urllib.parse import urljoin, quote
import argparse
import time

# ============================================================================
# CONFIGURATION
# ============================================================================

GITHUB_API_BASE = "https://api.github.com"
OUTPUT_FILE = "projects_analysis.json"
SCHEMA_FILE = "_schema.md"
CACHE_DIR = ".github_analyzer_cache"
RATE_LIMIT_PAUSE = 0.5  # seconds between API calls

# Tech stack detection patterns
TECH_STACK_PATTERNS = {
    "Python": r"(import|from)\s+(django|flask|fastapi|sqlalchemy|pandas|numpy|pytest)",
    "JavaScript": r"(require|import)\s+['\"]?(react|vue|angular|express|next|typescript)",
    "TypeScript": r"(import|from)\s+['\"].*\.(ts|tsx)['\"]|:\s*(string|number|boolean|interface)",
    "Docker": r"FROM\s+\w+|WORKDIR|RUN\s+",
    "Kubernetes": r"apiVersion:|kind:|metadata:|spec:",
    "AWS": r"(boto3|aws-sdk|cloudformation)",
    "GraphQL": r"(query|mutation|subscription|resolver)",
    "REST API": r"(route|endpoint|GET|POST|PUT|DELETE)",
    "Database": r"(sql|postgres|mysql|mongodb|redis|elasticsearch)",
    "Testing": r"(pytest|jest|mocha|unittest|rspec|xunit)",
    "CI/CD": r"(github actions|gitlab ci|jenkins|travis|circleci)",
}

COMMIT_MESSAGE_PATTERNS = {
    "fix": r"^(fix|bugfix|hotfix):",
    "feature": r"^(feat|feature|add):",
    "docs": r"^(docs|doc):",
    "refactor": r"^(refactor|refactoring):",
    "style": r"^(style|format):",
    "test": r"^(test|tests):",
    "ci": r"^(ci|chore):",
}

TEST_PATTERNS = [r".*test.*\.py$", r".*\.test\.js$", r".*\.spec\.js$", r"test/.*"]
CI_PATTERNS = [".github/workflows", ".gitlab-ci.yml", "Jenkinsfile", ".travis.yml", "azure-pipelines.yml"]
LINT_PATTERNS = [".eslintrc", "pyproject.toml", ".flake8", "tox.ini", ".pylintrc", "prettier.config.js"]

# ============================================================================
# UTILITIES
# ============================================================================

class GitHubAPI:
    """Wrapper for GitHub REST API with rate limit handling."""
    
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        }
        self.rate_limit_remaining = float('inf')
        self.rate_limit_reset = 0
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Any]:
        """Make API request with rate limit handling."""
        url = f"{GITHUB_API_BASE}{endpoint}"
        if params:
            query_string = "&".join(f"{k}={v}" for k, v in params.items())
            url = f"{url}?{query_string}"
        
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                if "X-RateLimit-Remaining" in response.headers:
                    self.rate_limit_remaining = int(response.headers["X-RateLimit-Remaining"])
                return data
        except urllib.error.HTTPError as e:
            if e.code == 403:
                reset_time = int(e.headers.get("X-RateLimit-Reset", time.time()))
                sleep_time = max(reset_time - time.time(), 0)
                print(f"⚠️  Rate limit hit. Sleeping for {sleep_time:.0f}s...", file=sys.stderr)
                time.sleep(sleep_time + 1)
                return self._make_request(endpoint, params)
            elif e.code == 404:
                return None
            else:
                print(f"❌ API Error ({e.code}): {e.reason}", file=sys.stderr)
                return None
        except Exception as e:
            print(f"⚠️  Request error: {e}", file=sys.stderr)
            return None
        finally:
            time.sleep(RATE_LIMIT_PAUSE)
    
    def get_user_repos(self) -> List[Dict]:
        """Fetch all repos for authenticated user."""
        repos = []
        page = 1
        while True:
            data = self._make_request("/user/repos", {"page": str(page), "per_page": "100"})
            if not data or isinstance(data, dict) and "message" in data:
                break
            if not isinstance(data, list):
                break
            repos.extend(data)
            if len(data) < 100:
                break
            page += 1
        return repos
    
    def get_repo_readme(self, owner: str, repo: str) -> Optional[str]:
        """Fetch README content."""
        data = self._make_request(f"/repos/{owner}/{repo}/readme")
        if data and "content" in data:
            import base64
            try:
                return base64.b64decode(data["content"]).decode()
            except:
                return None
        return None
    
    def get_commits(self, owner: str, repo: str, limit: int = 100) -> List[Dict]:
        """Fetch commit history."""
        commits = []
        page = 1
        per_page = min(100, limit)
        while len(commits) < limit:
            data = self._make_request(
                f"/repos/{owner}/{repo}/commits",
                {"page": str(page), "per_page": str(per_page)}
            )
            if not data or not isinstance(data, list):
                break
            commits.extend(data)
            if len(data) < per_page:
                break
            page += 1
        return commits[:limit]
    
    def get_issues(self, owner: str, repo: str, state: str = "all", limit: int = 50) -> List[Dict]:
        """Fetch issues (excluding PRs)."""
        issues = []
        page = 1
        per_page = min(100, limit)
        while len(issues) < limit:
            data = self._make_request(
                f"/repos/{owner}/{repo}/issues",
                {"state": state, "page": str(page), "per_page": str(per_page)}
            )
            if not data or not isinstance(data, list):
                break
            issues.extend([i for i in data if "pull_request" not in i])
            if len(data) < per_page:
                break
            page += 1
        return issues[:limit]
    
    def get_pull_requests(self, owner: str, repo: str, state: str = "all", limit: int = 50) -> List[Dict]:
        """Fetch pull requests."""
        prs = []
        page = 1
        per_page = min(100, limit)
        while len(prs) < limit:
            data = self._make_request(
                f"/repos/{owner}/{repo}/pulls",
                {"state": state, "page": str(page), "per_page": str(per_page)}
            )
            if not data or not isinstance(data, list):
                break
            prs.extend(data)
            if len(data) < per_page:
                break
            page += 1
        return prs[:limit]
    
    def get_file_content(self, owner: str, repo: str, path: str) -> Optional[str]:
        """Fetch file content."""
        data = self._make_request(f"/repos/{owner}/{repo}/contents/{quote(path)}")
        if data and "content" in data:
            import base64
            try:
                return base64.b64decode(data["content"]).decode()
            except:
                return None
        return None

# ============================================================================
# REPOSITORY ANALYZER
# ============================================================================

class RepositoryAnalyzer:
    """Analyze a single repository for detailed metrics."""
    
    def __init__(self, api: GitHubAPI):
        self.api = api
    
    def analyze(self, repo_data: Dict) -> Dict:
        """Perform comprehensive analysis of a repository."""
        owner = repo_data["owner"]["login"]
        repo_name = repo_data["name"]
        
        print(f"📊 Analyzing {owner}/{repo_name}...", file=sys.stderr)
        
        analysis = {
            "name": repo_data["name"],
            "full_name": repo_data["full_name"],
            "url": repo_data["html_url"],
            "description": repo_data.get("description", ""),
            "topics": repo_data.get("topics", []),
            "homepage": repo_data.get("homepage", ""),
            "language": repo_data.get("language", ""),
            "created_at": repo_data.get("created_at", ""),
            "updated_at": repo_data.get("updated_at", ""),
            "pushed_at": repo_data.get("pushed_at", ""),
            "size_kb": repo_data.get("size", 0),
            "stars_count": repo_data.get("stargazers_count", 0),
            "forks_count": repo_data.get("forks_count", 0),
            "open_issues_count": repo_data.get("open_issues_count", 0),
            "watchers_count": repo_data.get("watchers_count", 0),
            "license": repo_data.get("license", {}).get("name", "") if repo_data.get("license") else "",
            "default_branch": repo_data.get("default_branch", "main"),
            "archived": repo_data.get("archived", False),
            "disabled": repo_data.get("disabled", False),
        }
        
        readme_data = self._analyze_readme(owner, repo_name)
        analysis.update(readme_data)
        
        commits_data = self._analyze_commits(owner, repo_name)
        analysis.update(commits_data)
        
        issues_data = self._analyze_issues(owner, repo_name)
        analysis.update(issues_data)
        
        pr_data = self._analyze_prs(owner, repo_name)
        analysis.update(pr_data)
        
        quality_data = self._analyze_code_quality(owner, repo_name)
        analysis.update(quality_data)
        
        analysis["effectiveness_score"] = self._calculate_effectiveness_score(analysis)
        
        return analysis
    
    def _analyze_readme(self, owner: str, repo: str) -> Dict:
        """Extract README content and tech stack."""
        result = {
            "readme_preview": "",
            "readme_length": 0,
            "has_setup_section": False,
            "has_usage_section": False,
            "has_contribute_section": False,
            "detected_tech_stack": [],
        }
        
        try:
            readme = self.api.get_repo_readme(owner, repo)
            if readme:
                result["readme_length"] = len(readme)
                result["readme_preview"] = readme[:500]
                
                readme_lower = readme.lower()
                result["has_setup_section"] = any(s in readme_lower for s in ["setup", "installation", "install"])
                result["has_usage_section"] = any(s in readme_lower for s in ["usage", "quick start", "getting started"])
                result["has_contribute_section"] = any(s in readme_lower for s in ["contribute", "contributing"])
                
                for tech, pattern in TECH_STACK_PATTERNS.items():
                    if re.search(pattern, readme, re.IGNORECASE):
                        result["detected_tech_stack"].append(tech)
        except Exception as e:
            pass
        
        return result
    
    def _analyze_commits(self, owner: str, repo: str) -> Dict:
        """Analyze commit history."""
        result = {
            "total_commits": 0,
            "commits_last_6m": 0,
            "commits_per_month": 0.0,
            "unique_authors": 0,
            "commit_topics": {},
            "commit_frequency": "",
        }
        
        try:
            commits = self.api.get_commits(owner, repo, limit=100)
            result["total_commits"] = len(commits)
            
            if commits:
                six_months_ago = datetime.utcnow() - timedelta(days=180)
                authors = set()
                
                for commit in commits:
                    author = commit.get("commit", {}).get("author", {}).get("name", "unknown")
                    if author != "unknown":
                        authors.add(author)
                    
                    committed_at = commit.get("commit", {}).get("author", {}).get("date", "")
                    if committed_at:
                        try:
                            commit_date = datetime.fromisoformat(committed_at.replace("Z", "+00:00"))
                            if commit_date > six_months_ago:
                                result["commits_last_6m"] += 1
                        except:
                            pass
                    
                    message = commit.get("commit", {}).get("message", "").split("\n")[0].lower()
                    for topic, pattern in COMMIT_MESSAGE_PATTERNS.items():
                        if re.match(pattern, message):
                            result["commit_topics"][topic] = result["commit_topics"].get(topic, 0) + 1
                            break
                
                result["unique_authors"] = len(authors)
                
                if commits:
                    try:
                        first_date = datetime.fromisoformat(
                            commits[0]["commit"]["author"]["date"].replace("Z", "+00:00")
                        )
                        last_date = datetime.fromisoformat(
                            commits[-1]["commit"]["author"]["date"].replace("Z", "+00:00")
                        )
                        time_span = (first_date - last_date).days + 1
                        months = max(time_span / 30, 1)
                        result["commits_per_month"] = round(len(commits) / months, 2)
                        
                        if result["commits_per_month"] > 10:
                            result["commit_frequency"] = "very_active"
                        elif result["commits_per_month"] > 5:
                            result["commit_frequency"] = "active"
                        elif result["commits_per_month"] > 1:
                            result["commit_frequency"] = "moderate"
                        else:
                            result["commit_frequency"] = "minimal"
                    except:
                        pass
        except Exception as e:
            pass
        
        return result
    
    def _analyze_issues(self, owner: str, repo: str) -> Dict:
        """Analyze issues."""
        result = {
            "open_issues": 0,
            "closed_issues": 0,
            "issue_closure_rate": 0.0,
            "avg_issue_close_time_days": 0.0,
            "issue_labels": [],
        }
        
        try:
            open_issues = self.api.get_issues(owner, repo, state="open", limit=50)
            closed_issues = self.api.get_issues(owner, repo, state="closed", limit=50)
            
            result["open_issues"] = len(open_issues)
            result["closed_issues"] = len(closed_issues)
            
            if result["closed_issues"] + result["open_issues"] > 0:
                result["issue_closure_rate"] = round(
                    result["closed_issues"] / (result["closed_issues"] + result["open_issues"]) * 100, 2
                )
            
            close_times = []
            for issue in closed_issues:
                created = issue.get("created_at", "")
                closed = issue.get("closed_at", "")
                if created and closed:
                    try:
                        created_date = datetime.fromisoformat(created.replace("Z", "+00:00"))
                        closed_date = datetime.fromisoformat(closed.replace("Z", "+00:00"))
                        close_times.append((closed_date - created_date).days)
                    except:
                        pass
            
            if close_times:
                result["avg_issue_close_time_days"] = round(sum(close_times) / len(close_times), 1)
            
            all_labels = set()
            for issue in open_issues + closed_issues:
                for label in issue.get("labels", []):
                    all_labels.add(label.get("name", ""))
            result["issue_labels"] = sorted(list(all_labels))
        except Exception as e:
            pass
        
        return result
    
    def _analyze_prs(self, owner: str, repo: str) -> Dict:
        """Analyze pull requests."""
        result = {
            "merged_prs": 0,
            "open_prs": 0,
            "closed_prs": 0,
            "pr_merge_rate": 0.0,
            "avg_pr_review_comments": 0.0,
        }
        
        try:
            open_prs = self.api.get_pull_requests(owner, repo, state="open", limit=50)
            closed_prs = self.api.get_pull_requests(owner, repo, state="closed", limit=50)
            
            result["open_prs"] = len(open_prs)
            result["closed_prs"] = len(closed_prs)
            
            merged_count = sum(1 for pr in closed_prs if pr.get("merged_at"))
            result["merged_prs"] = merged_count
            
            if result["closed_prs"] > 0:
                abandoned = result["closed_prs"] - merged_count
                if abandoned > 0:
                    result["pr_merge_rate"] = round(result["merged_prs"] / result["closed_prs"] * 100, 2)
                else:
                    result["pr_merge_rate"] = 100.0
            
            review_counts = [pr.get("review_comments", 0) for pr in open_prs + closed_prs]
            if review_counts:
                result["avg_pr_review_comments"] = round(sum(review_counts) / len(review_counts), 2)
        except Exception as e:
            pass
        
        return result
    
    def _analyze_code_quality(self, owner: str, repo: str) -> Dict:
        """Analyze code quality indicators."""
        result = {
            "has_tests": False,
            "has_ci_config": False,
            "has_lint_config": False,
            "test_files_count": 0,
            "outdated_dependencies": [],
        }
        
        try:
            for ci_file in [".github/workflows", ".gitlab-ci.yml", "Jenkinsfile", ".travis.yml", "azure-pipelines.yml"]:
                content = self.api.get_file_content(owner, repo, ci_file)
                if content:
                    result["has_ci_config"] = True
                    break
            
            for lint_file in [".eslintrc.json", ".eslintrc.js", "pyproject.toml", ".flake8", "tox.ini"]:
                content = self.api.get_file_content(owner, repo, lint_file)
                if content:
                    result["has_lint_config"] = True
                    break
            
            # Check for tests
            for test_dir in ["test", "tests", "__tests__", "spec", "specs"]:
                content = self.api.get_file_content(owner, repo, test_dir)
                if content:
                    result["has_tests"] = True
                    break
            
            # Check dependency files
            for dep_file in ["package.json", "requirements.txt", "go.mod", "Gemfile", "pom.xml"]:
                content = self.api.get_file_content(owner, repo, dep_file)
                if content:
                    result["outdated_dependencies"] = self._check_outdated_deps(content, dep_file)
                    break
        except Exception as e:
            pass
        
        return result
    
    def _check_outdated_deps(self, content: str, filename: str) -> List[str]:
        """Parse dependency files and extract top packages."""
        outdated = []
        
        if "package.json" in filename:
            try:
                package = json.loads(content)
                deps = {**package.get("dependencies", {}), **package.get("devDependencies", {})}
                for pkg, version in list(deps.items())[:3]:
                    outdated.append(f"{pkg}@{version}")
            except:
                pass
        elif "requirements.txt" in filename:
            lines = content.split("\n")
            for line in lines[:3]:
                line = line.strip()
                if line and "==" in line:
                    outdated.append(line)
        
        return outdated
    
    def _calculate_effectiveness_score(self, analysis: Dict) -> int:
        """Calculate project effectiveness score (0-100)."""
        score = 0.0
        
        # 30% from activity
        activity_score = 0.0
        if analysis.get("commits_last_6m", 0) > 10:
            activity_score += 10
        elif analysis.get("commits_last_6m", 0) > 5:
            activity_score += 7
        else:
            activity_score += 2
        
        if analysis.get("issue_closure_rate", 0) > 80:
            activity_score += 10
        elif analysis.get("issue_closure_rate", 0) > 50:
            activity_score += 5
        
        if analysis.get("commits_last_6m", 0) > 0:
            activity_score += 10
        
        score += activity_score * 0.30
        
        # 30% from community
        community_score = 0.0
        if analysis.get("stars_count", 0) > 100:
            community_score += 15
        elif analysis.get("stars_count", 0) > 10:
            community_score += 8
        elif analysis.get("stars_count", 0) > 0:
            community_score += 3
        
        if analysis.get("forks_count", 0) > 5:
            community_score += 10
        elif analysis.get("forks_count", 0) > 0:
            community_score += 5
        
        if analysis.get("unique_authors", 0) > 5:
            community_score += 5
        
        score += community_score * 0.30
        
        # 20% from code health
        health_score = 0.0
        if analysis.get("has_tests"):
            health_score += 10
        if analysis.get("has_ci_config"):
            health_score += 5
        if analysis.get("has_lint_config"):
            health_score += 5
        
        score += health_score * 0.20
        
        # 20% from documentation
        doc_score = 0.0
        if analysis.get("readme_length", 0) > 1000:
            doc_score += 10
        elif analysis.get("readme_length", 0) > 500:
            doc_score += 5
        
        if analysis.get("has_setup_section") and analysis.get("has_usage_section"):
            doc_score += 10
        elif analysis.get("has_setup_section") or analysis.get("has_usage_section"):
            doc_score += 5
        
        score += doc_score * 0.20
        
        return int(score)

# ============================================================================
# MAIN ANALYZER
# ============================================================================

class PortfolioAnalyzer:
    """Main analyzer orchestrating the analysis of all repositories."""
    
    def __init__(self, token: str):
        self.api = GitHubAPI(token)
        self.analyzer = RepositoryAnalyzer(self.api)
        os.makedirs(CACHE_DIR, exist_ok=True)
    
    def analyze_all(self) -> List[Dict]:
        """Analyze all user repositories."""
        print("🔍 Fetching GitHub repositories...", file=sys.stderr)
        repos = self.api.get_user_repos()
        
        results = []
        skipped = []
        
        for i, repo in enumerate(repos, 1):
            try:
                if repo.get("archived"):
                    print(f"⏭️  Skipping {repo['name']} (archived)", file=sys.stderr)
                    skipped.append(repo["name"])
                    continue
                
                analysis = self.analyzer.analyze(repo)
                results.append(analysis)
                print(f"✅ {i}/{len(repos)} - {repo['name']}", file=sys.stderr)
            except Exception as e:
                print(f"❌ Error analyzing {repo.get('name', 'unknown')}: {e}", file=sys.stderr)
                skipped.append(repo.get("name", "unknown"))
        
        print(f"\n📊 Analysis complete: {len(results)} repos analyzed, {len(skipped)} skipped", file=sys.stderr)
        if skipped:
            print(f"⏭️  Skipped: {', '.join(skipped)}", file=sys.stderr)
        
        return results
    
    def save_results(self, results: List[Dict]) -> None:
        """Save results to JSON and schema to markdown."""
        # Sort by effectiveness score
        results = sorted(results, key=lambda x: x.get("effectiveness_score", 0), reverse=True)
        
        # Save JSON (minified)
        with open(OUTPUT_FILE, "w") as f:
            json.dump(results, f, separators=(',', ':'), default=str)
        print(f"\n💾 Results saved to {OUTPUT_FILE}", file=sys.stderr)
        
        # Save schema
        self._save_schema()
        print(f"📋 Schema saved to {SCHEMA_FILE}", file=sys.stderr)
    
    def _save_schema(self) -> None:
        """Generate and save schema documentation."""
        schema_content = """# GitHub Portfolio Analysis Schema

## Overview
This JSON file contains comprehensive metrics for assessing GitHub projects. Each object represents one repository analyzed, sorted by effectiveness_score (highest first).

## Field Descriptions

### Basic Repository Information
- `name` (string): Repository name
- `full_name` (string): Full repository path (owner/repo)
- `url` (string): GitHub repository URL
- `description` (string): Repository description
- `topics` (array): GitHub topics/tags
- `homepage` (string): Project homepage URL
- `language` (string): Primary programming language
- `created_at` (string): ISO 8601 creation timestamp
- `updated_at` (string): ISO 8601 last update timestamp
- `pushed_at` (string): ISO 8601 last commit timestamp
- `size_kb` (integer): Repository size in kilobytes
- `license` (string): License name (e.g., "MIT", "Apache-2.0")
- `default_branch` (string): Default branch name
- `archived` (boolean): Whether repository is archived
- `disabled` (boolean): Whether repository is disabled

### Community Metrics
- `stars_count` (integer): Number of stars/watchers
- `forks_count` (integer): Number of forks
- `open_issues_count` (integer): Number of open issues at fetch time
- `watchers_count` (integer): Number of watchers

### README Analysis
- `readme_preview` (string): First 500 characters of README
- `readme_length` (integer): Total README length in characters
- `has_setup_section` (boolean): README contains setup/installation instructions
- `has_usage_section` (boolean): README contains usage/quickstart examples
- `has_contribute_section` (boolean): README contains contribution guidelines
- `detected_tech_stack` (array): Technologies detected in README (e.g., "Python", "React", "Docker")

### Commit Analysis
- `total_commits` (integer): Total commits in repository (up to 100 fetched)
- `commits_last_6m` (integer): Commits made in last 6 months
- `commits_per_month` (number): Average commits per month across repo lifetime
- `commit_frequency` (string): Activity level: very_active (>10/month), active (>5/month), moderate (>1/month), minimal
- `unique_authors` (integer): Number of distinct commit authors
- `commit_topics` (object): Count of commits by type (fix, feature, docs, refactor, style, test, ci)

### Issues Analysis
- `open_issues` (integer): Number of open issues (up to 50 fetched)
- `closed_issues` (integer): Number of closed issues (up to 50 fetched)
- `issue_closure_rate` (number): Percentage of fetched issues that are closed (0-100)
- `avg_issue_close_time_days` (number): Average days to close a closed issue
- `issue_labels` (array): Common issue labels found (e.g., "bug", "enhancement", "help wanted")

### Pull Request Analysis
- `open_prs` (integer): Number of open pull requests (up to 50 fetched)
- `closed_prs` (integer): Number of closed pull requests (up to 50 fetched)
- `merged_prs` (integer): Number of merged pull requests
- `pr_merge_rate` (number): Percentage of closed PRs that were merged (0-100)
- `avg_pr_review_comments` (number): Average review comments per PR

### Code Quality Metrics
- `has_tests` (boolean): Repository contains test files or test directories
- `has_ci_config` (boolean): Repository has CI/CD configuration (.github/workflows, .gitlab-ci.yml, etc.)
- `has_lint_config` (boolean): Repository has linting/formatting configuration
- `test_files_count` (integer): Number of detected test files
- `outdated_dependencies` (array): Top 3 packages from dependency files (package.json, requirements.txt, etc.)

### Effectiveness Score
- `effectiveness_score` (integer): Composite score (0-100) based on:
  - **30% Activity**: commits in last 6 months + issue closure rate
  - **30% Community**: stars, forks, external contributors
  - **20% Code Health**: tests, CI/CD, linting
  - **20% Documentation**: README quality and completeness

## Usage for AI Analysis

### 1. Identify Strongest Technical Niches
```
- Group projects by detected_tech_stack (count frequency)
- Calculate avg effectiveness_score per technology
- Recommend specializing in top 3 tech stacks by impact
```

### 2. Prioritize Portfolio Projects
```
- Filter: effectiveness_score >= 70
- Filter: (stars_count > 10 OR forks_count > 5)
- Prioritize: has_tests AND has_ci_config
- These are top candidates for portfolio, case studies, and marketing
```

### 3. Identify Skill Gaps
```
- Find projects with has_tests = false (testing coverage gap)
- Find projects with has_ci_config = false (DevOps/CI gap)
- Count projects by language (underrepresented = skill gap)
- Recommend learning: missing testing frameworks, CI platforms, cloud services
```

### 4. Refactoring Candidates
```
- Low effectiveness_score (< 40) with stars_count > 5
- High outdated_dependencies count (> 2)
- has_tests = false with large codebase
- readme_length < 500 (documentation debt)
- These projects have high ROI for improvement
```

### 5. Freelance Case Study Candidates
```
- Filter: stars_count >= 50 OR forks_count >= 5
- Filter: effectiveness_score >= 65
- Must have: has_tests AND has_ci_config AND readme_length > 500
- Prioritize: projects solving specific business problems
- Action: Create detailed case studies (problem → solution → impact → metrics)
```

### 6. Project Ideation & Market Gaps
```
- Find underserved tech combinations (e.g., Python+GraphQL+Docker)
- Compare detected_tech_stack frequency vs market demand
- Identify emerging tech with few projects
- Recommend new projects to fill gaps and increase marketability
```

### 7. Engagement Analysis
```
- Projects with stars_count > 50 but effectiveness_score < 50 = revival candidates
- Projects with activity > median but stars < 10 = visibility/marketing opportunity
- High pr_merge_rate (>90%) + issue_closure_rate (>80%) = healthy community
```

### 8. Skill Assessment
```
- commits_per_month by language = expertise depth
- unique_authors = collaboration experience
- commit_topics distribution = work type (more fixes vs features?)
- Presence of CI/CD + tests + docs = professional development maturity
```
"""
        with open(SCHEMA_FILE, "w") as f:
            f.write(schema_content)

# ============================================================================
# CLI & ENTRY POINT
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Comprehensive GitHub portfolio analyzer for AI-driven assessment",
        epilog="Example: python github_portfolio_analyzer.py --token ghp_xxxxx"
    )
    parser.add_argument("--token", help="GitHub personal access token (or set GITHUB_TOKEN env var)")
    
    args = parser.parse_args()
    
    # Get token
    token = args.token or os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ Error: GitHub token required", file=sys.stderr)
        print("   Option 1: Set GITHUB_TOKEN environment variable", file=sys.stderr)
        print("   Option 2: Pass --token to command line", file=sys.stderr)
        print("\n📖 To create a token:", file=sys.stderr)
        print("   1. Go to https://github.com/settings/tokens", file=sys.stderr)
        print("   2. Click 'Generate new token (classic)'", file=sys.stderr)
        print("   3. Select 'repo' scope", file=sys.stderr)
        print("   4. Copy the token and use it with this script", file=sys.stderr)
        sys.exit(1)
    
    # Run analysis
    try:
        print("🚀 Starting GitHub Portfolio Analyzer...\n", file=sys.stderr)
        analyzer = PortfolioAnalyzer(token)
        results = analyzer.analyze_all()
        
        if results:
            analyzer.save_results(results)
            
            print(f"\n✨ Analysis complete!", file=sys.stderr)
            print(f"📄 Generated files:", file=sys.stderr)
            print(f"   - {OUTPUT_FILE} (JSON data)", file=sys.stderr)
            print(f"   - {SCHEMA_FILE} (Field documentation)", file=sys.stderr)
            print(f"\n💡 Next steps:", file=sys.stderr)
            print(f"   1. Review {SCHEMA_FILE} to understand the data structure", file=sys.stderr)
            print(f"   2. Use {OUTPUT_FILE} with your AI tool for portfolio assessment", file=sys.stderr)
            print(f"   3. Sort by 'effectiveness_score' to identify top projects", file=sys.stderr)
            print(f"   4. Check for skill gaps in has_tests and has_ci_config fields", file=sys.stderr)
        else:
            print("❌ No repositories found or analyzed", file=sys.stderr)
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  Analysis interrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
