# -*- coding: utf-8 -*-

from copy import copy
from copy import deepcopy
from itertools import chain
from functools import partial

import maya
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import UnicodeText
from sqlalchemy import func
from toolz.dicttoolz import dissoc

import sbds.sbds_logging
import sbds.sbds_json
from sbds.storages.db.tables import Base
from sbds.storages.db.utils import UniqueMixin
from sbds.utils import block_num_from_previous

logger = sbds.sbds_logging.getLogger(__name__)

from sqlalchemy.types import UnicodeText
from sqlalchemy.dialects import mysql
UT = UnicodeText()
UT= UT.with_variant(mysql.MEDIUMTEXT, 'mysql')

# pylint: disable=line-too-long
class Block(Base, UniqueMixin):
    """{
        "extensions": [],
        "timestamp": "2016-08-11T22:00:09",
        "transaction_merkle_root": "57e17f40cfa97c260eef365dc599e06acdba8591",
        "previous": "003d0900c38ca36625f50fc6724cbb9d82a9a93e",
        "witness": "roadscape",
        "transactions": [
            {
                "signatures": [
                    "1f7f99b4e98878ecd2b65bc9e6c8e2fc3a929fdb766411e89b6df2accddf326b901e8bc10c0d0f47738c26c6fdcf15f76a11eb69a12058e96820b2625061d6aa96"
                ],
                "extensions": [],
                "expiration": "2016-08-11T22:00:18",
                "ref_block_num": 2203,
                "operations": [
                    [
                        "comment",
                        {
                            "body": "@@ -154,16 +154,17 @@\n at coffe\n+e\n  deliver\n",
                            "title": "",
                            "author": "mindfreak",
                            "parent_author": "einsteinpotsdam",
                            "permlink": "re-einsteinpotsdam-tutorial-for-other-shop-owners-how-to-accept-steem-and-steem-usd-payments-setup-time-under-2-minutes-android-20160811t215904898z",
                            "parent_permlink": "tutorial-for-other-shop-owners-how-to-accept-steem-and-steem-usd-payments-setup-time-under-2-minutes-android",
                            "json_metadata": "{\"tags\":[\"steemit\"]}"
                        }
                    ]
                ],
                "ref_block_prefix": 3949810370
            },
            {
                "signatures": [],
                "extensions": [],
                "expiration": "2016-08-11T22:00:36",
                "ref_block_num": 2304,
                "operations": [
                    [
                        "witness_update",
                        {
                            "url": "http://fxxk.com",
                            "props": {
                                "maximum_block_size": 65536,
                                "account_creation_fee": "1.000 STEEM",
                                "sbd_interest_rate": 1000
                            },
                            "block_signing_key": "STM5b3wkzd5cPuW8tYbHpsM6qo26R5eympAQsBaoEfeMDxxUCLvsY",
                            "fee": "0.000 STEEM",
                            "owner": "supercomputing06"
                        }
                    ]
                ],
                "ref_block_prefix": 1721994435
            },
            {
                "signatures": [],
                "extensions": [],
                "expiration": "2016-08-11T22:00:36",
                "ref_block_num": 2304,
                "operations": [
                    [
                        "account_update",
                        {
                            "json_metadata": "",
                            "account": "supercomputing06",
                            "memo_key": "STM7myUzFgMrc5w2jRc3LH2cTwcs96q74Kj6GJ3DyKHyrHFPDP96N",
                            "active": {
                                "key_auths": [
                                    [
                                        "STM5sP9GUuExPzK35F1MLjN2dTY7fqqP7dSpMWqnzCoU3je64gm6q",
                                        2
                                    ],
                                    [
                                        "STM7t97bmNzbVruhH3yGQ7yFR58UJyPTb7Jh6ugmPfH1zqzJpngQH",
                                        1
                                    ]
                                ],
                                "weight_threshold": 0,
                                "account_auths": []
                            }
                        }
                    ]
                ],
                "ref_block_prefix": 1721994435
            },
            {
                "signatures": [],
                "extensions": [],
                "expiration": "2016-08-11T22:00:36",
                "ref_block_num": 2304,
                "operations": [
                    [
                        "account_update",
                        {
                            "json_metadata": "",
                            "account": "supercomputing06",
                            "memo_key": "STM7myUzFgMrc5w2jRc3LH2cTwcs96q74Kj6GJ3DyKHyrHFPDP96N",
                            "active": {
                                "key_auths": [
                                    [
                                        "STM5sP9GUuExPzK35F1MLjN2dTY7fqqP7dSpMWqnzCoU3je64gm6q",
                                        2
                                    ],
                                    [
                                        "STM7t97bmNzbVruhH3yGQ7yFR58UJyPTb7Jh6ugmPfH1zqzJpngQH",
                                        1
                                    ]
                                ],
                                "weight_threshold": 2,
                                "account_auths": []
                            }
                        }
                    ]
                ],
                "ref_block_prefix": 1721994435
            }
        ],
        "witness_signature": "20033915d9ddfca226eeadc57807556f18dd1ace85659774f2b6e620c56426e4560449e07635e9724ad1171a1f49800fe392e047e2a69bfbe9ee06948608fca211"
    }

    Args:

    Returns:

    """
    # pylint: enable=line-too-long
    __tablename__ = 'sbds_core_blocks'
    __table_args__ = ({
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_general_ci'
    }, )

    raw = Column(UT)
    block_num = Column(
        Integer, primary_key=True, nullable=False, autoincrement=False)
    previous = Column(Unicode(50))
    timestamp = Column(DateTime(timezone=False), index=True)
    witness = Column(Unicode(50))
    witness_signature = Column(Unicode(150))
    transaction_merkle_root = Column(Unicode(50))

    def __repr__(self):
        return "<Block(block_num='%s', timestamp='%s')>" % (self.block_num,
                                                            self.timestamp)

    def dump(self):
        return dissoc(self.__dict__, '_sa_instance_state')

    def to_dict(self, include_raw=False):
        data = self.dump()
        if not include_raw:
            return dissoc(data, 'raw')
        else:
            return data

    def to_json(self):
        return sbds.sbds_json.dumps(self.to_dict())

    @classmethod
    def _prepare_for_storage(cls, raw_block):
        """
        Convert raw block tp dict formatted for storage.

        Args:
            raw_block (Union[Dict[str, str], Dict[str, List]]):

        Returns:
            Union[Dict[str, str], Dict[str, int]]:
        """
        block = prepare_raw_block(raw_block)
        return dict(
            raw=block['raw'],
            block_num=block['block_num'],
            previous=block['previous'],
            timestamp=block['timestamp'],
            witness=block['witness'],
            witness_signature=block['witness_signature'],
            transaction_merkle_root=block['transaction_merkle_root'])

    @classmethod
    def get_or_create_from_raw_block(cls, raw_block, session=None):
        """
        Return Block instance from raw block, creating if necessary.

        Args:
            raw_block (Dict[str, str]):
            session (sqlalchemy.orm.session.Session):

        Returns:
            sbds.storages.db.tables.core.Block:
        """
        prepared = cls._prepare_for_storage(raw_block)
        return cls.as_unique(session, **prepared)

    @classmethod
    def from_raw_block(cls, raw_block):
        """
        Instantiate Block from raw block.

        Args:
            raw_block (Union[Dict[str, str], Dict[str, List]]):

        Returns:
            sbds.storages.db.tables.core.Block:
        """
        prepared = cls._prepare_for_storage(raw_block)
        return cls(**prepared)

    # pylint: disable=unused-argument
    @classmethod
    def unique_hash(cls, *args, **kwargs):
        return kwargs['block_num']

    @classmethod
    def unique_filter(cls, query, *args, **kwargs):
        return query.filter(cls.block_num == kwargs['block_num'])

    # pylint: enable=unused-argument

    @classmethod
    def highest_block(cls, session):
        """
        Return integer result of MAX(block_num) db query.

        This does not have the same meaning as last irreversible block, ie, it
        makes no claim that the all blocks lower than the MAX(block_num) exist
        in the database.

        Args:
            session (sqlalchemy.orm.session.Session):

        Returns:
            int:
        """
        highest = session.query(func.max(cls.block_num)).scalar()
        if not highest:
            return 0
        else:
            return highest

    @classmethod
    def count(cls, session, start=None, end=None):
        query = session.query(func.count(cls.timestamp)).with_hint(
            cls, 'USE INDEX(ix_sbds_core_blocks_timestamp)')
        if start is not None:
            query = query.filter(cls.block_num >= start)
        if end:
            query = query.filter(cls.block_num <= end)
        return query.scalar()

    @classmethod
    def count_missing(cls, session, last_chain_block):
        block_count = cls.count(session)
        return last_chain_block - block_count

    @classmethod
    def find_missing_range(cls, session, start, end):
        start = start or 1
        correct_range = range(start, end + 1)
        correct_block_count = (end + 1) - start
        actual_block_count = cls.count(session, start, end)
        if correct_block_count == actual_block_count:
            return []
        query = session.query(cls.block_num)
        query = query.filter(cls.block_num >= start, cls.block_num <= end)
        results = query.all()
        block_nums = (r.block_num for r in results)
        correct = set(correct_range)
        missing = correct.difference(block_nums)
        return missing

    @classmethod
    def get_missing_block_num_iterator(cls,
                                       session,
                                       last_chain_block,
                                       chunksize=100000):
        highest_block = cls.highest_block(session)
        # handle empty db case efficiently
        if highest_block == 0:
            num_chunks = (last_chain_block // chunksize) + 1
            chunks = []
            for i in range(1, num_chunks + 1):
                start = (i - 1) * chunksize
                if start == 0:
                    start = 1
                end = i * chunksize
                if end >= last_chain_block:
                    end = last_chain_block
                chunks.append(partial(range, start, end))
            return chunks
        else:
            num_chunks = (last_chain_block // chunksize) + 1
            chunks = []
            for i in range(1, num_chunks + 1):
                start = (i - 1) * chunksize
                end = i * chunksize
                if end >= last_chain_block:
                    end = last_chain_block
                chunks.append(
                    partial(cls.find_missing_range, session, start, end))
            return chunks

    @classmethod
    def find_missing(cls, session, last_chain_block, chunksize=1000000):
        missing_block_num_gen = cls.get_missing_block_num_iterator(
            session, last_chain_block, chunksize=chunksize)
        all_missing = []
        for missing_query in missing_block_num_gen:
            all_missing.extend(missing_query())
        return all_missing


def from_raw_block(raw_block, session=None):
    """
    Extract and instantiate Block and Txs from raw block.

    Args:
        raw_block (Dict[str, str]):
        session (sqlalchemy.orm.session.Session):

    Returns:
        Tuple[Block, List[TxBase,None])
    """
    # pylint: disable=redefined-variable-type
    from .tx import TxBase
    if session:
        block = Block.get_or_create_from_raw_block(raw_block, session=session)
    else:
        block = Block.from_raw_block(raw_block)
    tx_transactions = TxBase.from_raw_block(raw_block)
    return block, tx_transactions


def prepare_raw_block(raw_block):
    """
    Convert raw block to dict, adding block_num.

    Args:
        raw_block (Union[Dict[str, List], Dict[str, str]]):

    Returns:
        Union[Dict[str, List], None]:
    """
    block_dict = dict()
    if isinstance(raw_block, dict):
        block = deepcopy(raw_block)
        block_dict.update(**block)
        block_dict['raw'] = sbds.sbds_json.dumps(block, ensure_ascii=True)
    elif isinstance(raw_block, str):
        block_dict.update(**sbds.sbds_json.loads(raw_block))
        block_dict['raw'] = copy(raw_block)
    elif isinstance(raw_block, bytes):
        block = deepcopy(raw_block)
        raw = block.decode('utf8')
        block_dict.update(**sbds.sbds_json.loads(raw))
        block_dict['raw'] = copy(raw)
    else:
        raise TypeError('Unsupported raw block type')
    if 'block_num' not in block_dict:
        block_num = block_num_from_previous(block_dict['previous'])
        block_dict['block_num'] = block_num
    if isinstance(block_dict.get('timestamp'), str):
        timestamp = maya.dateparser.parse(block_dict['timestamp'])
        block_dict['timestamp'] = timestamp
    return block_dict


def extract_transactions_from_blocks(blocks):
    """

    Args:
        blocks ():

    Returns:

    """
    transactions = chain.from_iterable(
        map(extract_transactions_from_block, blocks))
    return transactions


def extract_transactions_from_block(_block):
    """

    Args:
        _block (Dict[str, str]):

    Returns:

    """
    block = prepare_raw_block(_block)
    block_transactions = deepcopy(block['transactions'])
    for transaction_num, original_tx in enumerate(block_transactions, 1):
        tx = deepcopy(original_tx)
        yield dict(
            block_num=block['block_num'],
            timestamp=block['timestamp'],
            transaction_num=transaction_num,
            ref_block_num=tx['ref_block_num'],
            ref_block_prefix=tx['ref_block_prefix'],
            expiration=tx['expiration'],
            type=tx['operations'][0][0],
            operations=tx['operations'])


def extract_operations_from_block(raw_block):
    """

    Args:
        raw_block (Dict[str, str]):

    Returns:
    """
    block = prepare_raw_block(raw_block)
    transactions = extract_transactions_from_block(block)
    for transaction in transactions:
        for op_num, _operation in enumerate(transaction['operations'], 1):
            operation = deepcopy(_operation)
            op_type, op = operation
            op.update(
                block_num=transaction['block_num'],
                transaction_num=transaction['transaction_num'],
                operation_num=op_num,
                timestamp=block['timestamp'],
                type=op_type)
            yield op


def extract_operations_from_blocks(blocks):
    """

    Args:
        blocks ():

    Returns:

    """
    operations = chain.from_iterable(
        map(extract_operations_from_block, blocks))
    return operations
