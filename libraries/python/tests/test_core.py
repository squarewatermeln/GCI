import unittest
from GCI.metric import GCIMath
from GCI.scanner import scan_function


class TestGCIMetric(unittest.TestCase):

    def test_linear_vs_quadratic_at_scale(self):
        """
        Verify that at Industrial Scale (1M), a light Quadratic function
        scores higher than a heavy Linear function.
        """
        # Algorithm A: 50n (Heavy Linear) -> X=50, Y=1
        linear_heavy = GCIMath.calculate_score(2.0, 50.0, 1.0)

        # Algorithm B: n^2 (Standard Quadratic) -> X=1, Y=2
        quadratic = GCIMath.calculate_score(2.0, 1.0, 2.0)

        print(
            f"\n[Test] Linear(50n): {linear_heavy:.2f} GCI vs Quad(n^2): {quadratic:.2f} GCI"
        )

        # In Log-Space, n^2 should be significantly heavier than 50n at 1M inputs
        self.assertTrue(quadratic > linear_heavy)

    def test_scanner_detection(self):
        """
        Test if the AST scanner correctly identifies nested loops.
        """
        code = """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
"""
        result = scan_function(code)

        # Should be Rank 2 (Polynomial)
        self.assertEqual(result["coordinate"][0], 2.0)
        # Should be Rate 2 (Nested Loops)
        self.assertEqual(result["coordinate"][2], 2.0)

        print(f"\n[Test] Scanner detected Bubble Sort as: {result['GCI_score']} GCI")


if __name__ == "__main__":
    unittest.main()
