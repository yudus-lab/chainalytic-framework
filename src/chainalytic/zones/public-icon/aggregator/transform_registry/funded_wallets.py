import json
import time
from typing import Dict, List, Optional, Set, Tuple, Union
import traceback

import plyvel
from iconservice.icon_config import default_icon_config
from iconservice.icon_constant import ConfigKey
from iconservice.iiss.engine import Engine

from chainalytic.aggregator.transform import BaseTransform
from chainalytic.common import rpc_client, trie


class Transform(BaseTransform):
    START_BLOCK_HEIGHT = 1

    LAST_STATE_HEIGHT_KEY = b'last_state_height'
    MAX_WALLETS = 200

    def __init__(self, working_dir: str, zone_id: str, transform_id: str):
        super(Transform, self).__init__(working_dir, zone_id, transform_id)

    async def execute(self, height: int, input_data: dict) -> Optional[Dict]:
        # Load transform cache to retrive previous staking state
        cache_db = self.transform_cache_db
        cache_db_batch = self.transform_cache_db.write_batch()

        # Make sure input block data represents for the next block of previous state cache
        prev_state_height = cache_db.get(Transform.LAST_STATE_HEIGHT_KEY)
        if prev_state_height:
            prev_state_height = int(prev_state_height)
            if prev_state_height != height - 1:
                await rpc_client.call_async(
                    self.warehouse_endpoint,
                    call_id='api_call',
                    api_id='set_last_block_height',
                    api_params={'height': prev_state_height, 'transform_id': self.transform_id},
                )
                return None

        # Create cache and storage data for genesis block 0
        if height == 1:
            cache_db_batch.put(b'hx54f7853dc6481b670caf69c5a27c7c8fe5be8269', b'800460000')
            cache_db_batch.put(b'hx1000000000000000000000000000000000000000', b'0')
            cache_db_batch.write()

            await rpc_client.call_async(
                self.warehouse_endpoint,
                call_id='api_call',
                api_id='update_funded_wallets',
                api_params={
                    'updated_wallets': {
                        'wallets': {
                            'hx54f7853dc6481b670caf69c5a27c7c8fe5be8269': '800460000',
                            'hx1000000000000000000000000000000000000000': '0',
                        },
                        'height': 0,
                    },
                    'transform_id': 'funded_wallets',
                },
            )

        # #################################################

        txs = input_data['data']

        # Example of `updated_wallets`
        # {
        #     "ADDRESS_1": "100000.0",
        #     "ADDRESS_2": "9999.9999",
        # }
        updated_wallets = {}

        for tx in txs:
            source_balance = cache_db.get(tx['from'].encode())
            dest_balance = cache_db.get(tx['to'].encode())
            value = tx['value']

            source_balance = float(source_balance) if source_balance else 0
            dest_balance = float(dest_balance) if dest_balance else 0
            if source_balance >= value:
                source_balance -= value
                dest_balance += value
                updated_wallets[tx['from']] = str(source_balance)
                updated_wallets[tx['to']] = str(dest_balance)

        for addr, balance in updated_wallets.items():
            cache_db_batch.put(addr.encode(), balance.encode())

        cache_db_batch.put(Transform.LAST_STATE_HEIGHT_KEY, str(height).encode())
        cache_db_batch.write()

        return {
            'height': height,
            'data': {},
            'misc': {'updated_wallets': {'wallets': updated_wallets, 'height': height}},
        }
