import time
from web3 import Web3
import json
from dotenv import load_dotenv
import os

# 读取环境变量
load_dotenv()
INFURA_KEY = os.getenv("INFURA_KEY")
BASE_REGISTRAR_ADDRESS = os.getenv("BASE_REGISTRAR_ADDRESS")

# 连接到以太坊主网
w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{INFURA_KEY}'))

# 加载 BaseRegistrarImplementation 合约 ABI
with open('base_registrar_abi.json', 'r') as f:
    base_registrar_abi = json.load(f)

# 创建合约实例
base_registrar = w3.eth.contract(address=BASE_REGISTRAR_ADDRESS, abi=base_registrar_abi)

# 查询 ENS 域名的到期时间
label = "testensdomain"  # 域名前缀
label_hash = w3.keccak(text=label)                # 得到 bytes
token_id = int.from_bytes(label_hash, 'big')      # 转为 uint256

try:
    expiry_timestamp = base_registrar.functions.nameExpires(token_id).call()
    if expiry_timestamp == 0:
        print(f"{label}.eth 尚未注册")
    else:
        expiry_date = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(expiry_timestamp))
        print(f"{label}.eth 过期时间：{expiry_date} (UTC)")
except Exception as e:
    print(f"查询失败: {e}")
