import os
import pytest
from chainalytic.common import config


def test_chain_registry_value(setup_chainalytic_config):
    data = config.get_chain_registry()
    assert data
    zones = data['zones']
    zones = {z['zone_id']: z for z in zones}

    assert 'public-icon' in zones
    z = zones['public-icon']
    assert z['zone_name'] == 'Public ICON mainnet'
    assert z['client_endpoint'] == 'localhost:9000'
    assert z['chain_db_dir'] == ''
    assert z['score_db_icondex_dir'] == ''
    assert z['direct_db_access'] == 0

    assert 'public-ethereum' in zones
    z = zones['public-ethereum']
    assert z['zone_name'] == 'Public Ethereum mainnet'
    assert z['client_endpoint'] == ''
    assert z['chain_db_dir'] == ''
    assert z['direct_db_access'] == 0


def test_setting_value(setup_chainalytic_config):
    setting = config.get_setting()
    assert setting
    valid_keys = [
        'upstream_endpoint',
        'aggregator_endpoint',
        'warehouse_endpoint',
        'provider_endpoint',
        'warehouse_dir',
        'zone_storage_dir',
        'transform_storage_dir',
        'transform_cache_dir',
    ]
    for k in valid_keys:
        assert k in setting

    assert setting['upstream_endpoint'] == 'localhost:5500'
    assert setting['aggregator_endpoint'] == 'localhost:5510'
    assert setting['warehouse_endpoint'] == 'localhost:5520'
    assert setting['provider_endpoint'] == 'localhost:5530'
    assert setting['warehouse_dir'] == '.chainalytic/chainalytic_warehouse'
    assert setting['zone_storage_dir'] == '{warehouse_dir}/{zone_id}_storage'
    assert setting['transform_storage_dir'] == '{zone_storage_dir}/{transform_id}_storage'
    assert setting['transform_cache_dir'] == '{zone_storage_dir}/{transform_id}_cache'

