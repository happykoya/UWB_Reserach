import struct

def binary_to_decimal(binary_str):
    # 2進数文字列をバイナリデータに変換
    binary_data = bytes.fromhex(binary_str)

    # バイナリデータを浮動小数点数に変換
    float_value = struct.unpack('f', binary_data)[0]
    return float_value

# テスト用の2進数文字列
binary_str = '52b8de3f'

# 10進数に変換して表示
decimal_value = binary_to_decimal(binary_str)
print(decimal_value)

import float_converter

data = 0x40490fdb224c7798  # 8バイトのデータ
result = float_converter.convert_to_float(data)
print("result:",result)