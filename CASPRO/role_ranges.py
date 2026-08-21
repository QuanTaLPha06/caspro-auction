# Lot-number ranges per pool section, exactly matching the structure of
# Mock_IPL_Auction_2026_Player_Pool.pdf (Batsmen / WK / All-rounders / Pace / Spin
# sub-sections within each of Pool A-E).

ROLE_RANGES = [
    # (pool, role, start_lot, end_lot)
    ("A", "BAT",  1,  14),
    ("A", "WK",   15, 28),
    ("A", "AR",   29, 42),   # note: 32 is unused, doesn't affect range lookup
    ("A", "PACE", 43, 56),
    ("A", "SPIN", 57, 70),

    ("B", "BAT",  71,  84),
    ("B", "WK",   85,  99),
    ("B", "AR",   100, 112),
    ("B", "PACE", 113, 126),
    ("B", "SPIN", 127, 140),

    ("C", "BAT",  141, 154),
    ("C", "WK",   155, 168),
    ("C", "AR",   169, 182),
    ("C", "PACE", 183, 196),
    ("C", "SPIN", 197, 210),

    ("D", "BAT",  211, 224),
    ("D", "WK",   225, 238),
    ("D", "AR",   239, 252),
    ("D", "PACE", 253, 266),
    ("D", "SPIN", 267, 280),

    ("E", "BAT",  281, 294),
    ("E", "WK",   295, 308),
    ("E", "AR",   309, 322),
    ("E", "PACE", 323, 336),
    ("E", "SPIN", 337, 350),
]


def get_role(lot: int) -> str:
    for pool, role, start, end in ROLE_RANGES:
        if start <= lot <= end:
            return role
    return "AR"  # fallback (covers lot 32, the intentionally-unused slot)
