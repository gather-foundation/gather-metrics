from scipy import stats  # type: ignore


def norm_from_percentiles(x1, p1, x2, p2):
    """Return a normal distribuion X parametrized by:

    P(X < p1) = x1
    P(X < p2) = x2
    """
    p1ppf = stats.norm.ppf(p1)
    p2ppf = stats.norm.ppf(p2)

    location = ((x1 * p2ppf) - (x2 * p1ppf)) / (p2ppf - p1ppf)
    scale = (x2 - x1) / (p2ppf - p1ppf)

    return location, scale
