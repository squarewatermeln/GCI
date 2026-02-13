import math


class GCIMath:
    """
    Core mathematical engine for the GCI Metric.
    Implements Level-Index Arithmetic with industrial reference loads.
    """

    STANDARD_LOAD = 1_000_000  # x = 10^6

    @staticmethod
    def calculate_score(rank: float, magnitude: float, rate: float) -> float:
        """
        Calculates the Standard GCI Score (GCI_1M).
        """
        # Safety for log domain
        safe_mag = max(magnitude, 1.0)
        safe_rate = max(rate, 1.0)
        safe_x = max(GCIMath.STANDARD_LOAD, 1.0)

        # Heuristic Value Calculation (Linear Interpolation of Complexity Class)
        try:
            val_low, val_high = 0.0, 0.0

            # Helper to compute raw cost at integer ranks
            def raw_cost(r):
                if r == 0:
                    return safe_mag
                if r == 1:
                    return safe_mag * math.log(safe_x, 2)
                if r == 2:
                    return safe_mag * (safe_x**safe_rate)
                if r == 3:
                    try:
                        return (max(safe_mag, 1.1)) ** (safe_x**safe_rate)
                    except OverflowError:
                        return float("inf")
                return float("inf")

            lower = int(math.floor(rank))
            fraction = rank - lower

            v_low = raw_cost(lower)
            v_high = raw_cost(lower + 1)

            # Log-Space Blending
            if v_low <= 0:
                v_low = 1e-9
            if v_high <= 0:
                v_high = 1e-9

            log_blend = (1 - fraction) * math.log(v_low) + fraction * math.log(v_high)

            # The GCI Formula: M = R + log10(Gradient)
            # We approximate Gradient via the blended log value
            gradient = math.log10(max(1, math.exp(log_blend)))

            return round(float(rank + gradient), 4)

        except (ValueError, OverflowError):
            return float("inf")
