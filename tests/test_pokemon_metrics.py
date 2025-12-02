import pytest

from app.services.pokemon_transformer import compute_metrics


def test_compute_metrics_pikachu_like_data():
    fake_poke_data = {
        "id": 25,
        "stats": [
            {"base_stat": 35, "stat": {"name": "hp"}},
            {"base_stat": 55, "stat": {"name": "attack"}},
            {"base_stat": 40, "stat": {"name": "defense"}},
            {"base_stat": 50, "stat": {"name": "special-attack"}},
            {"base_stat": 50, "stat": {"name": "special-defense"}},
            {"base_stat": 90, "stat": {"name": "speed"}},
        ],
    }

    metrics = compute_metrics(fake_poke_data)

    assert metrics["pokedex_id"] == 25
    assert metrics["base_hp"] == 35
    assert metrics["base_attack"] == 55
    assert metrics["base_defense"] == 40
    assert metrics["base_special_attack"] == 50
    assert metrics["base_special_defense"] == 50
    assert metrics["base_speed"] == 90

    assert metrics["total_base_stats"] == 320
    assert metrics["power_index"] == pytest.approx(399.5)
    assert metrics["tier"] == "C"
