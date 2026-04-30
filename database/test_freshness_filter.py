"""
Test suite for the RAG pipeline freshness filter
Tests the is_job_fresh() function with various date formats and edge cases
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.pinecone_retriever import is_job_fresh


class TestJobFreshnessFilter(unittest.TestCase):
    """
    Unit tests for job freshness filtering.
    
    A job is considered "fresh" if it was posted within the last month.
    Jobs with 'month', 'months', 'year', or 'years' are filtered out as stale.
    """
    
    # ═══════════════════════════════════════════════════════════
    # TEST FRESH JOBS (should return True)
    # ═══════════════════════════════════════════════════════════
    
    def test_fresh_posted_today(self):
        """Job posted today should be fresh"""
        job = {"posted": "today"}
        self.assertTrue(is_job_fresh(job), "Job posted today should be fresh")
    
    def test_fresh_posted_now(self):
        """Job posted now should be fresh"""
        job = {"posted": "now"}
        self.assertTrue(is_job_fresh(job), "Job posted now should be fresh")
    
    def test_fresh_posted_recently(self):
        """Job posted recently should be fresh"""
        job = {"posted": "recently"}
        self.assertTrue(is_job_fresh(job), "Job posted recently should be fresh")
    
    def test_fresh_posted_hour_ago(self):
        """Job posted 1 hour ago should be fresh"""
        job = {"posted": "1 hour ago"}
        self.assertTrue(is_job_fresh(job), "Job posted 1 hour ago should be fresh")
    
    def test_fresh_posted_hours_ago(self):
        """Job posted 3 hours ago should be fresh"""
        job = {"posted": "3 hours ago"}
        self.assertTrue(is_job_fresh(job), "Job posted 3 hours ago should be fresh")
    
    def test_fresh_posted_minute_ago(self):
        """Job posted 15 minutes ago should be fresh"""
        job = {"posted": "15 minutes ago"}
        self.assertTrue(is_job_fresh(job), "Job posted 15 minutes ago should be fresh")
    
    def test_fresh_posted_day_ago(self):
        """Job posted 1 day ago should be fresh"""
        job = {"posted": "1 day ago"}
        self.assertTrue(is_job_fresh(job), "Job posted 1 day ago should be fresh")
    
    def test_fresh_posted_days_ago(self):
        """Job posted 5 days ago should be fresh"""
        job = {"posted": "5 days ago"}
        self.assertTrue(is_job_fresh(job), "Job posted 5 days ago should be fresh")
    
    def test_fresh_posted_week_ago(self):
        """Job posted 1 week ago should be fresh"""
        job = {"posted": "1 week ago"}
        self.assertTrue(is_job_fresh(job), "Job posted 1 week ago should be fresh")
    
    def test_fresh_posted_weeks_ago(self):
        """Job posted 3 weeks ago should be fresh"""
        job = {"posted": "3 weeks ago"}
        self.assertTrue(is_job_fresh(job), "Job posted 3 weeks ago should be fresh")
    
    def test_fresh_with_time_field(self):
        """Should check 'time' field if 'posted' is missing"""
        job = {"time": "2 days ago"}
        self.assertTrue(is_job_fresh(job), "Should accept jobs with 'time' field")
    
    def test_fresh_with_date_field(self):
        """Should check 'date' field if posted/time are missing"""
        job = {"date": "3 hours ago"}
        self.assertTrue(is_job_fresh(job), "Should accept jobs with 'date' field")
    
    # ═══════════════════════════════════════════════════════════
    # TEST STALE JOBS (should return False)
    # ═══════════════════════════════════════════════════════════
    
    def test_stale_posted_1_month_ago(self):
        """Job posted 1 month ago should be stale"""
        job = {"posted": "1 month ago"}
        self.assertFalse(is_job_fresh(job), "Job posted 1 month ago should be stale")
    
    def test_stale_posted_2_months_ago(self):
        """Job posted 2 months ago should be stale"""
        job = {"posted": "2 months ago"}
        self.assertFalse(is_job_fresh(job), "Job posted 2 months ago should be stale")
    
    def test_stale_posted_6_months_ago(self):
        """Job posted 6 months ago should be stale"""
        job = {"posted": "6 months ago"}
        self.assertFalse(is_job_fresh(job), "Job posted 6 months ago should be stale")
    
    def test_stale_posted_1_year_ago(self):
        """Job posted 1 year ago should be stale"""
        job = {"posted": "1 year ago"}
        self.assertFalse(is_job_fresh(job), "Job posted 1 year ago should be stale")
    
    def test_stale_posted_2_years_ago(self):
        """Job posted 2 years ago should be stale"""
        job = {"posted": "2 years ago"}
        self.assertFalse(is_job_fresh(job), "Job posted 2 years ago should be stale")
    
    # ═══════════════════════════════════════════════════════════
    # TEST EDGE CASES
    # ═══════════════════════════════════════════════════════════
    
    def test_case_insensitivity(self):
        """Filter should be case-insensitive"""
        job1 = {"posted": "1 Month ago"}  # Capital M
        job2 = {"posted": "2 MONTHS AGO"}  # All caps
        self.assertFalse(is_job_fresh(job1), "Should filter case-insensitive 'Month'")
        self.assertFalse(is_job_fresh(job2), "Should filter case-insensitive 'MONTHS'")
    
    def test_missing_posted_field(self):
        """If no posted/time/date field, default to fresh"""
        job = {"title": "Software Engineer", "company": "Google"}
        self.assertTrue(is_job_fresh(job), "Jobs without date info should default to fresh")
    
    def test_na_value(self):
        """Jobs with 'N/A' date should be kept (default to fresh)"""
        job = {"posted": "N/A"}
        self.assertTrue(is_job_fresh(job), "Jobs with 'N/A' date should be kept")
    
    def test_empty_posted_field(self):
        """Empty posted field should default to fresh"""
        job = {"posted": ""}
        self.assertTrue(is_job_fresh(job), "Empty posted field should default to fresh")
    
    def test_whitespace_in_posted(self):
        """Should handle whitespace in posted field"""
        job = {"posted": "  1 month ago  "}  # Extra whitespace
        self.assertFalse(is_job_fresh(job), "Should handle whitespace in 'month' detection")
    
    def test_numeric_month(self):
        """Should not filter out numeric dates without 'month' keyword"""
        job = {"posted": "2024-03-15"}
        self.assertTrue(is_job_fresh(job), "Numeric dates without 'month' keyword should pass")
    
    def test_boundary_month_exactly(self):
        """Job posted exactly 1 month ago"""
        job = {"posted": "1 month"}
        self.assertFalse(is_job_fresh(job), "Job with '1 month' should be filtered")
    
    def test_multiple_sources_priority(self):
        """Should prioritize posted > time > date"""
        # If posted has "2 days ago", it should be used regardless of time/date
        job = {"posted": "2 days ago", "time": "6 months ago", "date": "1 year ago"}
        self.assertTrue(is_job_fresh(job), "Should use 'posted' field priority")


class TestFreshnessFilterIntegration(unittest.TestCase):
    """
    Integration tests for freshness filter with realistic job data.
    """
    
    def test_realistic_fresh_job(self):
        """Test with realistic fresh job data"""
        job = {
            "title": "Senior Python Developer",
            "company": "Google",
            "location": "Cairo, Egypt",
            "posted": "2 days ago",
            "description": "Join our team..."
        }
        self.assertTrue(is_job_fresh(job), "Realistic fresh job should pass")
    
    def test_realistic_stale_job(self):
        """Test with realistic stale job data"""
        job = {
            "title": "Senior Python Developer",
            "company": "Google",
            "location": "Cairo, Egypt",
            "posted": "3 months ago",
            "description": "Join our team..."
        }
        self.assertFalse(is_job_fresh(job), "Realistic stale job should be filtered")
    
    def test_batch_filtering(self):
        """Test filtering a batch of jobs"""
        jobs = [
            {"title": "Job 1", "posted": "1 day ago"},      # Fresh
            {"title": "Job 2", "posted": "2 months ago"},   # Stale
            {"title": "Job 3", "posted": "3 hours ago"},    # Fresh
            {"title": "Job 4", "posted": "1 year ago"},     # Stale
            {"title": "Job 5", "posted": "2 weeks ago"},    # Fresh
        ]
        
        fresh = [j for j in jobs if is_job_fresh(j)]
        stale = [j for j in jobs if not is_job_fresh(j)]
        
        self.assertEqual(len(fresh), 3, "Should find 3 fresh jobs")
        self.assertEqual(len(stale), 2, "Should find 2 stale jobs")


# ═══════════════════════════════════════════════════════════
# PERFORMANCE TESTS
# ═══════════════════════════════════════════════════════════

class TestFreshnessFilterPerformance(unittest.TestCase):
    """Test performance of the freshness filter on large datasets."""
    
    def test_large_batch_performance(self):
        """Test filtering performance on 10,000 jobs"""
        import time
        
        # Create 10k jobs
        jobs = [
            {"posted": "2 days ago" if i % 2 == 0 else "6 months ago"}
            for i in range(10000)
        ]
        
        # Measure filtering time
        start = time.time()
        fresh_jobs = [j for j in jobs if is_job_fresh(j)]
        elapsed = time.time() - start
        
        # Should complete in < 1 second
        self.assertLess(elapsed, 1.0, f"Filtering 10k jobs should be fast, took {elapsed:.3f}s")
        self.assertEqual(len(fresh_jobs), 5000, "Should filter half the jobs correctly")


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
