#!/usr/bin/env python3
"""
Simple test for job freshness filter without model dependencies
"""

def is_job_fresh(job_dict):
    """
    Check if a job is recent (within 1 month).
    Filters out jobs with 'month', 'months', 'year', 'years' in posted date.
    """
    posted_val = job_dict.get('posted') or job_dict.get('time') or job_dict.get('date') or "N/A"
    posted_str = str(posted_val).lower().strip()
    
    # Filter out old jobs
    if any(old_marker in posted_str for old_marker in ['month', 'months', 'year', 'years']):
        return False
    
    # Accept fresh indicators
    if any(fresh_marker in posted_str for fresh_marker in ['day', 'days', 'week', 'weeks', 'hour', 'hours', 'minute', 'minutes', 'recently', 'now', 'today']):
        return True
    
    # Default: keep (if we can't determine, better to include)
    return True


def main():
    """Run freshness filter tests."""
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  JOB FRESHNESS FILTER TESTS  ".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70)
    
    test_cases = [
        {
            "job": {"title": "Python Dev", "posted": "2 days ago"},
            "expected": True,
            "description": "Recent job (2 days)"
        },
        {
            "job": {"title": "JS Dev", "posted": "1 week ago"},
            "expected": True,
            "description": "Recent job (1 week)"
        },
        {
            "job": {"title": "Data Scientist", "posted": "2 months ago"},
            "expected": False,
            "description": "Old job (2 months)"
        },
        {
            "job": {"title": "ML Engineer", "posted": "1 year ago"},
            "expected": False,
            "description": "Very old job (1 year)"
        },
        {
            "job": {"title": "DevOps", "posted": "3 hours ago"},
            "expected": True,
            "description": "Very recent job (3 hours)"
        },
        {
            "job": {"title": "QA Engineer", "posted": "1 month ago"},
            "expected": False,
            "description": "Exactly 1 month old"
        },
        {
            "job": {"title": "Product Manager", "posted": "Recently"},
            "expected": True,
            "description": "Recently posted"
        },
        {
            "job": {"title": "Sales", "posted": "Now"},
            "expected": True,
            "description": "Just posted"
        },
        {
            "job": {"title": "Backend Dev", "time": "5 days ago"},
            "expected": True,
            "description": "Using 'time' field instead of 'posted'"
        },
        {
            "job": {"title": "Frontend Dev", "date": "3 weeks ago"},
            "expected": True,
            "description": "Using 'date' field instead of 'posted'"
        },
    ]
    
    passed = 0
    failed = 0
    
    print("\n🧪 Running freshness filter tests...\n")
    
    for i, test_case in enumerate(test_cases, 1):
        job = test_case["job"]
        expected = test_case["expected"]
        description = test_case["description"]
        
        result = is_job_fresh(job)
        status = "✅ PASS" if result == expected else "❌ FAIL"
        
        print(f"{i}. {description}")
        print(f"   Job: {job.get('title', 'N/A')}")
        print(f"   Posted: {job.get('posted') or job.get('time') or job.get('date', 'N/A')}")
        print(f"   Expected: {expected}, Got: {result} {status}")
        
        if result == expected:
            passed += 1
        else:
            failed += 1
    
    print(f"\n{'─'*70}")
    print(f"✅ Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    
    print("\n" + "="*70)
    if failed == 0:
        print("✅ All freshness filter tests passed!")
    else:
        print(f"❌ {failed} test(s) failed!")
    print("="*70 + "\n")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    exit(main())
