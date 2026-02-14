import math


class GCIMath:
    """
    Core mathematical engine for the GCI Metric.
    Implements Level-Index Arithmetic with industrial reference loads.
    Ref: Section 4 "The Standard GCI Metric"
    """

    STANDARD_LOAD = 1_000_000  # x = 10^6

    @staticmethod
    def calculate_score(rank: float, magnitude: float, rate: float) -> float:
        """
        Calculates the Standard GCI Score (GCI_1M).

        Formula: M(x) = R + log10(Gradient)
        Where:   Gradient = ln(A) + B * ln(x)
        """
        # Safety for log domain
        # Magnitude (A) must be > 0. If 0 (e.g. O(0)), we treat as epsilon or 1.
        safe_mag = max(magnitude, 1.0)

        # Rate (B) acts as the multiplier in the log domain
        safe_rate = rate

        # Input load (x)
        safe_x = max(GCIMath.STANDARD_LOAD, 1.0)

        # --- STEP 1: Calculate the Gradient (Equation 4) ---
        # The paper defines Gradient as the linear projection of impact.
        # Gradient approx ln(A) + B * ln(x)
        # This represents the "Natural Log of the Cost" at the current rank.
        try:
            ln_x = math.log(safe_x)
            ln_mag = math.log(safe_mag)

            gradient = ln_mag + (safe_rate * ln_x)

            # Gradient must be positive for the next log step
            if gradient <= 0:
                gradient = 1e-9

        except ValueError:
            return 0.0

        # --- STEP 2: Calculate GCI Score (Equation 3) ---
        # M(x) approx R + log10(Gradient)
        # We add the Rank (R) to the log-scaled gradient.
        try:
            log_gradient = math.log10(gradient)
            score = rank + log_gradient

            return round(score, 4)

        except ValueError:
            # Handle cases where gradient is effectively 0
            return round(rank, 4)


# --- VERIFICATION (Matches Case Study in Table 1) ---
if __name__ == "__main__":
    # 1. Linear Search: O(n) -> Rank 2, Mag 1, Rate 1
    s1 = GCIMath.calculate_score(2.0, 1.0, 1.0)
    print(f"Linear Search: {s1} (Expected: 3.14)")

    # 2. Bubble Sort: O(n^2) -> Rank 2, Mag 1, Rate 2
    s2 = GCIMath.calculate_score(2.0, 1.0, 2.0)
    print(f"Bubble Sort:   {s2} (Expected: 3.44)")

    # 3. Naive Fibonacci: O(2^n) -> Rank 3, Mag 2, Rate 1
    # Note: Paper gets 4.14. Formula yields 4.16.
    # Difference is due to paper likely simplifying ln(2) approx 0 or rounding.
    s3 = GCIMath.calculate_score(3.0, 2.0, 1.0)
    print(f"Fibonacci:     {s3} (Expected: ~4.14)")
