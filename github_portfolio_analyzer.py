#!/usr/bin/env python3
"""
GitHub Portfolio Analyzer
Extracts detailed metrics from GitHub repositories to assess market relevance,
technical skill proficiency, code quality, and effectiveness for portfolio building.

Usage:
    python github_portfolio_analyzer.py [--token YOUR_TOKEN] [--local PATH]

Environment Variables:
    GITHUB_TOKEN: Personal access token (repo scope)
    LOCAL_REPO_PATH: Optional path to local repositories folder
"""

import os
import sys
import json
import re
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict, Counter
from urllib.parse import quote
import hashlib
import time

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError:
    print("ERROR: requests library required. Install with: pip install requests")
    sys.exit(1)


class GitHubAnalyzer:
    """Analyzes GitHub repositories and generates portfolio metrics."""
    
    BASE_URL = "https://api.github.com"
    CACHE_FILE = ".github_analyzer_cache.json"
    CACHE_EXPIRY = 3600  # 1 hour in seconds
    
    # Tech stack detection patterns
    TECH_PATTERNS = {
        'React': r'\breact\b|ReactDOM|@react|next\.js',
        'Vue': r'\bvue\b|vuex|nuxt',
        'Angular': r'\b@angular|ng-',
        'TypeScript': r'\btypescript\b|\.ts|\.tsx',
        'Python': r'\bpython\b|django|flask|fastapi|pandas|numpy',
        'Node.js': r'\bnode\.js\b|express|fastify',
        'Django': r'\bdjango\b',
        'Flask': r'\bflask\b',
        'FastAPI': r'\bfastapi\b',
        'PostgreSQL': r'\bpostgres|psycopg',
        'MongoDB': r'\bmongodb|mongoose|pymongo',
        'Docker': r'\bdocker\b|dockerfile',
        'Kubernetes': r'\bkubernetes|k8s',
        'AWS': r'\bamazon|aws|boto3|s3|lambda',
        'GCP': r'\bgoogle cloud|gcp|firebase',
        'GraphQL': r'\bgraphql',
        'REST API': r'\brest\b|api',
        'Git': r'\bgit\b',
        'GitHub Actions': r'\.github\/workflows',
        'GitLab CI': r'\.gitlab-ci\.yml',
        'Jenkins': r'\bjenkins\b|Jenkinsfile',
        'pytest': r'\bpytest\b',
        'Jest': r'\bjest\b',
        'Mocha': r'\bmocha\b',
        'RSpec': r'\brspec\b',
        'Webpack': r'\bwebpack',
        'Vite': r'\bvite',
        'ESLint': r'\beslint',
        'Prettier': r'\bprettier',
        'Black': r'\bblack\b',
        'Docker Compose': r'\bdocker-compose',
    }
    
    TEST_INDICATORS = [
        '__tests__', 'test', 'tests', 'spec', 'specs',
        'pytest.ini', 'setup.cfg', 'tox.ini', 'jest.config', 'karma.conf'
    ]
    
    CI_INDICATORS = {
        'GitHub Actions': '.github/workflows',
        'GitLab CI': '.gitlab-ci.yml',
        'Travis CI': '.travis.yml',
        'Circle CI': '.circleci/config.yml',
        'Jenkins': 'Jenkinsfile',
    }
    
    LINT_INDICATORS = {
        'ESLint': '.eslintrc',
        'Prettier': '.prettierrc',
        'Black': 'pyproject.toml',
        'Flake8': '.flake8',
        'Pylint': '.pylintrc',
    }
    
    def __init__(self, token: Optional[str] = None):
        """Initialize GitHub analyzer with authentication."""
        self.token = token or os.getenv('GITHUB_TOKEN')
        if not self.token:
            self.token = input("Enter your GitHub Personal Access Token: ").strip()
        
        self.session = self._create_session()
        self.cache = self._load_cache()
        self.rate_limit_remaining = 5000
        self.username = None
        self._get_authenticated_user()
    
    def _create_session(self) -> requests.Session:
        """Create requests session with retry strategy."""
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.headers.update({
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json',
        })
        return session
    
    def _load_cache(self) -> Dict:
        """Load cached API responses."""
        if Path(self.CACHE_FILE).exists():
            try:
                with open(self.CACHE_FILE, 'r') as f:
                    cache_data = json.load(f)
                    # Remove expired entries
                    current_time = time.time()
                    return {
                        k: v for k, v in cache_data.items()
                        if current_time - v.get('timestamp', 0) < self.CACHE_EXPIRY
                    }
            except Exception as e:
                print(f"Warning: Could not load cache: {e}")
        return {}
    
    def _save_cache(self):
        """Save cache to disk."""
        try:
            with open(self.CACHE_FILE, 'w') as f:
                json.dump(self.cache, f)
        except Exception as e:
            print(f"Warning: Could not save cache: {e}")
    
    def _get_cached(self, key: str) -> Optional[Any]:
        """Retrieve item from cache."""
        if key in self.cache:
            return self.cache[key].get('data')
        return None
    
    def _set_cached(self, key: str, data: Any):
        """Store item in cache."""
        self.cache[key] = {
            'data': data,
            'timestamp': time.time()
        }
    
    def _api_call(self, endpoint: str, method: str = 'GET', 
                  params: Optional[Dict] = None, **kwargs) -> Optional[Dict]:
        """Make API call with caching and rate limit handling."""
        # Check cache first
        cache_key = hashlib.md5(f"{method}:{endpoint}:{json.dumps(params or {})}".encode()).hexdigest()
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached
        
        try:
            url = f"{self.BASE_URL}{endpoint}"
            response = self.session.request(method, url, params=params, **kwargs)
            
            # Update rate limit
            if 'X-RateLimit-Remaining' in response.headers:
                self.rate_limit_remaining = int(response.headers['X-RateLimit-Remaining'])
            
            if response.status_code == 404:
                return None
            
            response.raise_for_status()
            data = response.json()
            self._set_cached(cache_key, data)
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"API Error ({endpoint}): {e}")
            return None
    
    def _get_paginated(self, endpoint: str, params: Optional[Dict] = None, 
                       per_page: int = 100, max_pages: int = 10) -> List[Dict]:
        """Fetch paginated API results."""
        results = []
        params = params or {}
        params['per_page'] = min(per_page, 100)
        
        for page in range(1, max_pages + 1):
            params['page'] = page
            data = self._api_call(endpoint, params=params)
            
            if not data:
                break
            
            # Handle both list and dict responses
            if isinstance(data, list):
                results.extend(data)
            elif isinstance(data, dict) and 'items' in data:
                results.extend(data['items'])
            else:
                break
            
            # Stop if we got fewer results than requested
            if isinstance(data, list) and len(data) < params['per_page']:
                break
        
        return results
    
    def _get_authenticated_user(self):
        """Get current authenticated user."""
        user_data = self._api_call('/user')
        if user_data:
            self.username = user_data.get('login')
            print(f"Authenticated as: {self.username}")
    
    def get_user_repos(self) -> List[Dict]:
        """Fetch all repositories for authenticated user."""
        print(f"\nFetching repositories for {self.username}...")
        repos = self._get_paginated('/user/repos', {'type': 'all'}, max_pages=100)
        print(f"Found {len(repos)} repositories")
        return repos
    
    def analyze_repo(self, repo: Dict) -> Dict:
        """Analyze a single repository."""
        repo_name = repo['name']
        full_name = repo['full_name']
        print(f"  Analyzing {full_name}...")
        
        analysis = {
            'name': repo_name,
            'full_name': full_name,
            'description': repo.get('description') or '',
            'topics': repo.get('topics') or [],
            'homepage': repo.get('homepage') or '',
            'language': repo.get('language') or '',
            'created_at': repo.get('created_at'),
            'updated_at': repo.get('updated_at'),
            'pushed_at': repo.get('pushed_at'),
            'size_kb': repo.get('size'),
            'stars_count': repo.get('stargazers_count', 0),
            'forks_count': repo.get('forks_count', 0),
            'open_issues_count': repo.get('open_issues_count', 0),
            'watchers_count': repo.get('watchers_count', 0),
            'license': repo.get('license', {}).get('name') or '',
            'default_branch': repo.get('default_branch'),
            'archived': repo.get('archived', False),
            'disabled': repo.get('disabled', False),
            'url': repo.get('html_url'),
        }
        
        # Skip archived/disabled repos for detailed analysis
        if analysis['archived'] or analysis['disabled']:
            print(f"    Skipping (archived/disabled)")
            return analysis
        
        # README preview
        analysis['readme_preview'] = self._extract_readme_preview(full_name)
        
        # Tech stack detection
        analysis['detected_tech'] = self._detect_tech_stack(full_name, analysis['readme_preview'])
        
        # Commits analysis
        commits_data = self._analyze_commits(full_name)
        analysis.update(commits_data)
        
        # Issues analysis
        issues_data = self._analyze_issues(full_name)
        analysis.update(issues_data)
        
        # Pull requests analysis
        pr_data = self._analyze_prs(full_name)
        analysis.update(pr_data)
        
        # Code quality
        quality_data = self._analyze_code_quality(full_name)
        analysis.update(quality_data)
        
        # Effectiveness score
        analysis['effectiveness_score'] = self._calculate_effectiveness_score(analysis)
        
        return analysis
    
    def _extract_readme_preview(self, full_name: str) -> str:
        """Extract first 500 chars from README."""
        readme_data = self._api_call(f'/repos/{full_name}/readme')
        if not readme_data:
            return ''
        
        try:
            # README content is base64 encoded
            import base64
            content = base64.b64decode(readme_data.get('content', '')).decode('utf-8')
            return content[:500].replace('\n', ' ')
        except Exception as e:
            return ''
    
    def _detect_tech_stack(self, full_name: str, readme: str) -> List[str]:
        """Detect technology stack from README and repo files."""
        detected = set()
        combined_text = readme.lower()
        
        # Get package.json, requirements.txt, go.mod
        for filename in ['package.json', 'requirements.txt', 'go.mod', 'Gemfile', 'pom.xml']:
            file_data = self._api_call(f'/repos/{full_name}/contents/{filename}')
            if file_data:
                try:
                    import base64
                    content = base64.b64decode(file_data.get('content', '')).decode('utf-8')
                    combined_text += ' ' + content.lower()
                except:
                    pass
        
        # Match patterns
        for tech, pattern in self.TECH_PATTERNS.items():
            if re.search(pattern, combined_text, re.IGNORECASE):
                detected.add(tech)
        
        return sorted(list(detected))
    
    def _analyze_commits(self, full_name: str) -> Dict:
        """Analyze commits."""
        commits = self._get_paginated(f'/repos/{full_name}/commits', max_pages=5)
        
        total_commits = len(commits)
        authors = set()
        topics = Counter()
        
        for commit in commits:
            if commit.get('author'):
                authors.add(commit['author'].get('login'))
            
            msg = commit.get('commit', {}).get('message', '').lower()
            if 'fix' in msg or 'bug' in msg:
                topics['fix'] += 1
            elif 'feature' in msg or 'add' in msg or 'feat' in msg:
                topics['feature'] += 1
            elif 'doc' in msg or 'readme' in msg:
                topics['docs'] += 1
            elif 'refactor' in msg:
                topics['refactor'] += 1
            elif 'test' in msg:
                topics['test'] += 1
        
        # Calculate commits per month
        if commits:
            oldest = datetime.fromisoformat(commits[-1]['commit']['author']['date'].replace('Z', '+00:00'))
            newest = datetime.fromisoformat(commits[0]['commit']['author']['date'].replace('Z', '+00:00'))
            months_diff = max((newest - oldest).days / 30, 1)
            commits_per_month = total_commits / months_diff
        else:
            commits_per_month = 0
        
        return {
            'total_commits': total_commits,
            'commits_per_month': round(commits_per_month, 2),
            'unique_authors': len(authors),
            'commit_topics': dict(topics.most_common(5)),
        }
    
    def _analyze_issues(self, full_name: str) -> Dict:
        """Analyze issues."""
        issues = self._get_paginated(
            f'/repos/{full_name}/issues',
            {'state': 'all'},
            max_pages=5
        )
        
        # Filter out pull requests
        issues = [i for i in issues if 'pull_request' not in i]
        
        open_count = sum(1 for i in issues if i['state'] == 'open')
        closed_count = sum(1 for i in issues if i['state'] == 'closed')
        
        labels_counter = Counter()
        close_times = []
        
        for issue in issues:
            # Count labels
            for label in issue.get('labels', []):
                labels_counter[label.get('name')] += 1
            
            # Calculate time to close
            if issue['state'] == 'closed' and issue.get('closed_at'):
                created = datetime.fromisoformat(issue['created_at'].replace('Z', '+00:00'))
                closed = datetime.fromisoformat(issue['closed_at'].replace('Z', '+00:00'))
                close_times.append((closed - created).days)
        
        avg_close_time = round(sum(close_times) / len(close_times), 1) if close_times else 0
        
        return {
            'open_issues': open_count,
            'closed_issues': closed_count,
            'issue_close_rate': round(closed_count / (open_count + closed_count) * 100, 1) if (open_count + closed_count) > 0 else 0,
            'avg_issue_close_days': avg_close_time,
            'top_issue_labels': dict(labels_counter.most_common(5)),
        }
    
    def _analyze_prs(self, full_name: str) -> Dict:
        """Analyze pull requests."""
        prs = self._get_paginated(
            f'/repos/{full_name}/pulls',
            {'state': 'all'},
            max_pages=5
        )
        
        merged_count = sum(1 for pr in prs if pr.get('merged_at'))
        abandoned_count = sum(1 for pr in prs if pr['state'] == 'closed' and not pr.get('merged_at'))
        
        review_comments = []
        for pr in prs:
            if pr.get('review_comments'):
                review_comments.append(pr['review_comments'])
        
        avg_review_comments = round(sum(review_comments) / len(review_comments), 1) if review_comments else 0
        
        return {
            'total_prs': len(prs),
            'merged_prs': merged_count,
            'abandoned_prs': abandoned_count,
            'pr_merge_rate': round(merged_count / len(prs) * 100, 1) if prs else 0,
            'avg_pr_review_comments': avg_review_comments,
        }
    
    def _analyze_code_quality(self, full_name: str) -> Dict:
        """Analyze code quality indicators."""
        quality = {
            'has_tests': False,
            'has_ci': [],
            'has_linting': [],
            'lines_of_code': 0,
            'file_count': 0,
            'avg_file_size_kb': 0,
        }
        
        # Get repo tree
        tree = self._api_call(f'/repos/{full_name}/git/trees/HEAD', params={'recursive': '1'})
        if not tree:
            return quality
        
        files = tree.get('tree', [])
        quality['file_count'] = len([f for f in files if f['type'] == 'blob'])
        
        # Check for test directories
        for f in files:
            path_lower = f['path'].lower()
            if any(test_dir in path_lower for test_dir in self.TEST_INDICATORS):
                quality['has_tests'] = True
                break
        
        # Check for CI
        for ci_name, ci_path in self.CI_INDICATORS.items():
            if any(ci_path in f['path'] for f in files):
                quality['has_ci'].append(ci_name)
        
        # Check for linting
        for lint_name, lint_file in self.LINT_INDICATORS.items():
            if any(lint_file in f['path'] for f in files):
                quality['has_linting'].append(lint_name)
        
        # Calculate LOC (estimate from file sizes)
        blob_files = [f for f in files if f['type'] == 'blob']
        if blob_files:
            size_sum = sum(f.get('size', 0) for f in blob_files)
            quality['file_count'] = len(blob_files)
            quality['avg_file_size_kb'] = round(size_sum / len(blob_files) / 1024, 2) if blob_files else 0
        
        return quality
    
    def _calculate_effectiveness_score(self, analysis: Dict) -> float:
        """Calculate effectiveness score (0-100)."""
        score = 0
        
        # Activity score (30%)
        activity_score = 0
        commits_recent = analysis.get('commits_per_month', 0)
        activity_score += min(commits_recent / 2 * 20, 20)  # Up to 20 for activity
        
        issue_close_rate = analysis.get('issue_close_rate', 0)
        activity_score += min(issue_close_rate / 5, 10)  # Up to 10 for issue closure
        
        score += activity_score
        
        # Community score (30%)
        community_score = 0
        stars = analysis.get('stars_count', 0)
        community_score += min(stars / 50, 15)  # Up to 15 for stars
        
        forks = analysis.get('forks_count', 0)
        community_score += min(forks / 10, 10)  # Up to 10 for forks
        
        unique_authors = analysis.get('unique_authors', 0)
        community_score += min((unique_authors - 1) / 10, 5)  # Up to 5 for external contributors
        
        score += min(community_score, 30)
        
        # Code health (20%)
        health_score = 0
        if analysis.get('has_tests'):
            health_score += 10
        if analysis.get('has_ci'):
            health_score += 5
        if analysis.get('has_linting'):
            health_score += 5
        
        score += health_score
        
        # Documentation (20%)
        doc_score = 0
        readme_len = len(analysis.get('readme_preview', ''))
        doc_score += min(readme_len / 100, 20)
        
        score += doc_score
        
        return min(round(score, 1), 100)
    
    def analyze_all(self) -> List[Dict]:
        """Analyze all user repositories."""
        repos = self.get_user_repos()
        analyses = []
        
        for repo in repos:
            try:
                analysis = self.analyze_repo(repo)
                analyses.append(analysis)
                time.sleep(0.1)  # Rate limit friendly
            except Exception as e:
                print(f"    Error analyzing {repo['name']}: {e}")
        
        return analyses
    
    def export_json(self, analyses: List[Dict], filename: str = 'projects_analysis.json'):
        """Export analysis to minified JSON."""
        with open(filename, 'w') as f:
            json.dump(analyses, f, separators=(',', ':'))
        print(f"\nExported analysis to {filename}")
    
    def export_schema(self, filename: str = '_schema.md'):
        """Export schema documentation."""
        schema_md = """# Projects Analysis Schema

## Overview
This JSON file contains comprehensive analysis of GitHub repositories for portfolio assessment and AI-driven project evaluation.

## Field Definitions

### Repository Metadata
- `name` (string): Repository name
- `full_name` (string): Owner/repo format
- `description` (string): Repository description
- `topics` (array): Repository topics/tags
- `homepage` (string): Project homepage URL
- `language` (string): Primary programming language
- `url` (string): Repository URL on GitHub
- `created_at` (ISO 8601): Repository creation date
- `updated_at` (ISO 8601): Last metadata update
- `pushed_at` (ISO 8601): Last commit date
- `size_kb` (integer): Repository size in KB
- `archived` (boolean): Is repository archived
- `disabled` (boolean): Is repository disabled

### Community Metrics
- `stars_count` (integer): GitHub stars
- `forks_count` (integer): Number of forks
- `open_issues_count` (integer): Open issues
- `watchers_count` (integer): Repository watchers
- `license` (string): License type

### Content Analysis
- `readme_preview` (string): First 500 chars of README
- `detected_tech` (array): Detected technology stack

### Commit Analysis
- `total_commits` (integer): Total commit count
- `commits_per_month` (float): Average commits per month
- `unique_authors` (integer): Number of unique authors
- `commit_topics` (object): Frequency of commit message types (fix, feature, docs, etc.)

### Issue Management
- `open_issues` (integer): Currently open issues
- `closed_issues` (integer): Resolved issues
- `issue_close_rate` (float): % of issues resolved
- `avg_issue_close_days` (float): Average days to close an issue
- `top_issue_labels` (object): Most frequently used issue labels

### Pull Request Management
- `total_prs` (integer): Total pull requests
- `merged_prs` (integer): Successfully merged PRs
- `abandoned_prs` (integer): Closed without merging
- `pr_merge_rate` (float): % of PRs merged
- `avg_pr_review_comments` (float): Average review comments per PR

### Code Quality Indicators
- `has_tests` (boolean): Presence of test files
- `has_ci` (array): Detected CI/CD systems (GitHub Actions, GitLab CI, etc.)
- `has_linting` (array): Detected linting tools (ESLint, Black, Flake8, etc.)
- `file_count` (integer): Total file count
- `avg_file_size_kb` (float): Average file size
- `lines_of_code` (integer): Estimated lines of code

### Effectiveness Score
- `effectiveness_score` (float, 0-100): Composite score calculated as:
  - 30% from activity (commits/month + issue closure rate)
  - 30% from community (stars, forks, external contributors)
  - 20% from code health (tests, CI, linting)
  - 20% from documentation (README length)

## AI Usage Guide

### Identify Technical Niches
- Group projects by `detected_tech` and `language`
- Analyze `effectiveness_score` per technology stack
- Identify which technologies have the highest community engagement

### Portfolio Optimization
- Projects with `effectiveness_score` > 70 are portfolio-ready
- Projects with low score but strong `total_commits` may need documentation
- High `stars_count` projects should be featured prominently

### Code Quality Assessment
- Missing `has_tests`? Suggest adding test coverage
- Missing `has_ci`? Recommend CI/CD setup
- Low `avg_pr_review_comments`? Indicate collaboration opportunity

### Skill Proficiency
- `commits_per_month` → Indicates activity level
- `unique_authors` → Collaboration skills
- `commit_topics` distribution → Breadth of work (fix vs feature vs docs)

### Gap Analysis
- Compare `detected_tech` across all projects
- Identify missing modern tech stacks
- Suggest complementary projects to build

### Upwork Client Appeal
- High `effectiveness_score` projects → Enterprise/stable client work
- Multiple languages/frameworks → Full-stack capability
- Strong `pr_merge_rate` and `avg_pr_review_comments` → Team player
"""
        
        with open(filename, 'w') as f:
            f.write(schema_md)
        print(f"Exported schema to {filename}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='GitHub Portfolio Analyzer')
    parser.add_argument('--token', help='GitHub Personal Access Token')
    parser.add_argument('--output', default='projects_analysis.json', help='Output JSON filename')
    parser.add_argument('--schema', default='_schema.md', help='Schema documentation filename')
    
    args = parser.parse_args()
    
    try:
        analyzer = GitHubAnalyzer(token=args.token)
        analyses = analyzer.analyze_all()
        analyzer.export_json(analyses, args.output)
        analyzer.export_schema(args.schema)
        
        print(f"\n{'='*60}")
        print(f"Analysis complete!")
        print(f"{'='*60}")
        print(f"Total repositories analyzed: {len(analyses)}")
        
        # Summary statistics
        avg_score = sum(a.get('effectiveness_score', 0) for a in analyses) / len(analyses) if analyses else 0
        print(f"Average effectiveness score: {avg_score:.1f}/100")
        
        top_projects = sorted(analyses, key=lambda x: x.get('effectiveness_score', 0), reverse=True)[:3]
        print(f"\nTop 3 Projects:")
        for i, proj in enumerate(top_projects, 1):
            print(f"  {i}. {proj['name']} ({proj.get('effectiveness_score', 0)}/100)")
        
        print(f"\nFiles generated:")
        print(f"  - {args.output}")
        print(f"  - {args.schema}")
        
    except KeyboardInterrupt:
        print("\nAborted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
