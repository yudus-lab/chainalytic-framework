import json
from pprint import pprint
from typing import Dict, List, Optional, Set, Tuple, Union

from chainalytic.common import config, rpc_client
from chainalytic.provider.collator import BaseCollator


class Collator(BaseCollator):
    def __init__(self, working_dir: str, zone_id: str):
        super(Collator, self).__init__(working_dir, zone_id)

    async def get_block(
        self, height: int, transform_id: str
    ) -> Optional[Union[Dict, str, float, int, bytes]]:
        r = await rpc_client.call_async(
            self.warehouse_endpoint,
            call_id='api_call',
            api_id='get_block',
            api_params={'height': height, 'transform_id': transform_id},
        )
        if r['status'] and r['data']:
            try:
                return json.loads(r['data'])
            except:
                return None
        else:
            return None

    async def last_block_height(self, transform_id: str) -> Optional[int]:
        r = await rpc_client.call_async(
            self.warehouse_endpoint,
            call_id='api_call',
            api_id='last_block_height',
            api_params={'transform_id': transform_id},
        )
        if r['status'] and r['data']:
            try:
                return int(r['data'])
            except:
                return None
        else:
            return None

    ####################################
    # For `stake_history` transform only
    #
    async def latest_unstake_state(self, transform_id: str) -> Optional[dict]:
        r = await rpc_client.call_async(
            self.warehouse_endpoint,
            call_id='api_call',
            api_id='latest_unstake_state',
            api_params={'transform_id': transform_id},
        )
        if r['status']:
            return r['data']
        else:
            self.logger.error('Failed to request data from Warehouse')
            self.logger.error(r['data'])
            return None

    ####################################
    # For `stake_top100` transform only
    #
    async def latest_stake_top100(self, transform_id: str) -> Optional[dict]:
        r = await rpc_client.call_async(
            self.warehouse_endpoint,
            call_id='api_call',
            api_id='latest_stake_top100',
            api_params={'transform_id': transform_id},
        )
        if r['status']:
            return r['data']
        else:
            self.logger.error('Failed to request data from Warehouse')
            self.logger.error(r['data'])
            return None

    ###########################################
    # For `recent_stake_wallets` transform only
    #
    async def recent_stake_wallets(self, transform_id: str) -> Optional[dict]:
        r = await rpc_client.call_async(
            self.warehouse_endpoint,
            call_id='api_call',
            api_id='recent_stake_wallets',
            api_params={'transform_id': transform_id},
        )
        if r['status']:
            return r['data']
        else:
            self.logger.error('Failed to request data from Warehouse')
            self.logger.error(r['data'])
            return None

    #######################################
    # For `abstention_stake` transform only
    #
    async def abstention_stake(self, transform_id: str) -> Optional[dict]:
        r = await rpc_client.call_async(
            self.warehouse_endpoint,
            call_id='api_call',
            api_id='abstention_stake',
            api_params={'transform_id': transform_id},
        )
        if r['status']:
            return r['data']
        else:
            self.logger.error('Failed to request data from Warehouse')
            self.logger.error(r['data'])
            return None

    #####################################
    # For `funded_wallets` transform only
    #
    async def funded_wallets(self, transform_id: str, min_balance: float) -> Optional[dict]:
        r = await rpc_client.call_async(
            self.warehouse_endpoint,
            call_id='api_call',
            api_id='funded_wallets',
            api_params={'transform_id': transform_id, 'min_balance': min_balance},
        )
        if r['status']:
            return r['data']
        else:
            self.logger.error('Failed to request data from Warehouse')
            self.logger.error(r['data'])
            return None

    ############################################
    # For `passive_stake_wallets` transform only
    #
    async def passive_stake_wallets(
        self, transform_id: str, max_inactive_duration: int
    ) -> Optional[dict]:
        r = await rpc_client.call_async(
            self.warehouse_endpoint,
            call_id='api_call',
            api_id='passive_stake_wallets',
            api_params={
                'transform_id': transform_id,
                'max_inactive_duration': max_inactive_duration,
            },
        )
        if r['status']:
            return r['data']
        else:
            self.logger.error('Failed to request data from Warehouse')
            self.logger.error(r['data'])
            return None
