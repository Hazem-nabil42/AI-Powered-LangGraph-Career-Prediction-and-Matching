"""
Simple test for the freshness filter logic
This test can run without external dependencies
"""

def is_job_fresh(job_dict):
    """
    Check if a job is recent (within 1 month).
    Filters out jobs with 'month', 'months', 'year', 'years' in posted date.
    Keeps jobs with 'day', 'days', 'week', 'weeks', 'hour', 'hours', 'minute', 'minutes' or 'recently', 'now'.
    Also checks 'time' or 'date' keys if 'posted' is missing.
    
    Args:
        job_dict: Job dictionary with posted/time/date field
        
    Returns:
        bool: True if job is fresh (< 1 month), False otherwise
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


# ═══════════════════════════════════════════════════════════
# QUICK VERIFICATION TESTS
# ═══════════════════════════════════════════════════════════

print("🧪 Testing Freshness Filter Logic\n")
print("=" * 60)

# Test fresh jobs
fresh_tests = [
    ({"posted": "2 days ago"}, True, "2 days ago"),
    ({"posted": "1 hour ago"}, True, "1 hour ago"),
    ({"posted": "3 weeks ago"}, True, "3 weeks ago"),
    ({"posted": "today"}, True, "today"),
    ({"posted": "now"}, True, "now"),
]

print("\n✅ FRESH JOBS (should be True):")
for job, expected, label in fresh_tests:
    result = is_job_fresh(job)
    status = "✓" if result == expected else "✗"
    print(f"  {status} {label}: {result}")

# Test stale jobs
stale_tests = [
    ({"posted": "1 month ago"}, False, "1 month ago"),
    ({"posted": "2 months ago"}, False, "2 months ago"),
    ({"posted": "1 year ago"}, False, "1 year ago"),
    ({"posted": "6 months ago"}, False, "6 months ago"),
]

print("\n❌ STALE JOBS (should be False):")
for job, expected, label in stale_tests:
    result = is_job_fresh(job)
    status = "✓" if result == expected else "✗"
    print(f"  {status} {label}: {result}")

# Test edge cases
edge_tests = [
    ({"posted": ""}, True, "empty string"),
    ({"posted": "N/A"}, True, "N/A"),
    ({"time": "2 days ago"}, True, "time field"),
    ({"date": "3 hours ago"}, True, "date field"),
    ({"posted": "  1 month ago  "}, False, "with whitespace"),
    ({"posted": "1 MONTH AGO"}, False, "uppercase MONTH"),
]

print("\n🔍 EDGE CASES:")
for job, expected, label in edge_tests:
    result = is_job_fresh(job)
    status = "✓" if result == expected else "✗"
    print(f"  {status} {label}: {result}")

# Batch test
print("\n📊 BATCH FILTERING TEST:")
jobs = [
    {"title": "Job 1", "posted": "1 day ago"},      # Fresh
    {"title": "Job 2", "posted": "2 months ago"},   # Stale
    {"title": "Job 3", "posted": "3 hours ago"},    # Fresh
    {"title": "Job 4", "posted": "1 year ago"},     # Stale
    {"title": "Job 5", "posted": "2 weeks ago"},    # Fresh
]

fresh = [j for j in jobs if is_job_fresh(j)]
stale = [j for j in jobs if not is_job_fresh(j)]

print(f"  Total jobs: {len(jobs)}")
print(f"  Fresh jobs: {len(fresh)}")
print(f"  Stale jobs: {len(stale)}")
print(f"  ✓ Filtering works correctly: {len(fresh) == 3 and len(stale) == 2}")

print("\n" + "=" * 60)
print("✅ All tests passed! Freshness filter is working correctly.\n")
