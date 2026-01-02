"""
Captain's Union Link Simulation v0.1

Simulates long-term behavior of a union uplink:
- Satellite + Cellular + Pager broadcast (fallback receive)
- Key rotation and occasional failures
- 1-year and 10-year handshake reliability

This is a conceptual model for stress-testing the Union Uplink Protocol.
"""

import random
from dataclasses import dataclass
from enum import Enum
from typing import Dict


class Link(Enum):
    CELLULAR = "cellular"
    SATELLITE = "satellite"
    PAGER_BROADCAST = "pager_broadcast"


@dataclass
class LinkStats:
    attempts: int = 0
    successes: int = 0
    failures: int = 0


@dataclass
class SimulationResult:
    total_steps: int
    total_handshakes: int
    success_count: int
    failure_count: int
    by_link: Dict[Link, LinkStats]


def link_available(base_availability: float, degradation: float, year: int) -> bool:
    """
    Determine if a link is available at a given year,
    based on base probability and yearly degradation.
    """
    effective = max(0.0, base_availability - degradation * year)
    return random.random() < effective


def handshake_success(availability_ok: bool, base_success: float) -> bool:
    """
    Given that the link is available, determine if handshake succeeds.
    """
    if not availability_ok:
        return False
    return random.random() < base_success


def simulate_union_links(
    years: int,
    steps_per_day: int = 144,   # one handshake every 10 minutes
    key_rotation_days: int = 30,
    initial_year: int = 0
) -> SimulationResult:
    """
    Simulate multi-year behavior of satellite + cellular union uplink.
    """
    base_availability = {
        Link.CELLULAR: 0.96,
        Link.SATELLITE: 0.98,
        Link.PAGER_BROADCAST: 0.995,
    }

    yearly_degradation = {
        Link.CELLULAR: 0.002,
        Link.SATELLITE: 0.001,
        Link.PAGER_BROADCAST: 0.0005,
    }

    base_success_prob = {
        Link.CELLULAR: 0.995,
        Link.SATELLITE: 0.993,
        Link.PAGER_BROADCAST: 0.999,  # verification only
    }

    by_link_stats: Dict[Link, LinkStats] = {link: LinkStats() for link in Link}

    total_steps = years * 365 * steps_per_day
    total_handshakes = 0
    success_count = 0
    failure_count = 0

    current_key_epoch = 0
    key_valid = True

    for step in range(total_steps):
        day = step / steps_per_day
        year = initial_year + int(day // 365)

        # Key rotation
        if day % key_rotation_days == 0 and step != 0:
            current_key_epoch += 1
            # 0.1% chance of rotation-induced key issue
            key_valid = random.random() > 0.001

        # We attempt one handshake per step
        total_handshakes += 1

        link_order = [Link.SATELLITE, Link.CELLULAR]

        handshake_done = False
        handshake_ok = False

        for link in link_order:
            av = link_available(
                base_availability[link],
                yearly_degradation[link],
                year
            )
            by_link_stats[link].attempts += 1

            if not av:
                by_link_stats[link].failures += 1
                continue

            if not key_valid:
                by_link_stats[link].failures += 1
                continue

            ok = handshake_success(av, base_success_prob[link])
            if ok:
                by_link_stats[link].successes += 1
                handshake_done = True
                handshake_ok = True
                break
            else:
                by_link_stats[link].failures += 1

        if handshake_done and handshake_ok:
            success_count += 1
        else:
            failure_count += 1

    return SimulationResult(
        total_steps=total_steps,
        total_handshakes=total_handshakes,
        success_count=success_count,
        failure_count=failure_count,
        by_link=by_link_stats,
    )


if __name__ == "__main__":
    random.seed(42)  # for repeatability

    # 1-year test
    year1 = simulate_union_links(years=1)
    print("=== 1-Year Simulation ===")
    print(f"Total handshakes: {year1.total_handshakes}")
    print(f"Success: {year1.success_count}, Failure: {year1.failure_count}")
    for link, stats in year1.by_link.items():
        print(f"[1-year] {link.value}: attempts={stats.attempts}, "
              f"successes={stats.successes}, failures={stats.failures}")

    # 10-year test
    year10 = simulate_union_links(years=10)
    print("\n=== 10-Year Simulation ===")
    print(f"Total handshakes: {year10.total_handshakes}")
    print(f"Success: {year10.success_count}, Failure: {year10.failure_count}")
    for link, stats in year10.by_link.items():
        print(f"[10-year] {link.value}: attempts={stats.attempts}, "
              f"successes={stats.successes}, failures={stats.failures}")
