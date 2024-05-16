class Binary32:
    def __init__(self, bin32_str):
        str_ = bin32_str
    
        if len(str_) == 8:
            # 16進数表記の場合は2進数表記へ変換
            str_ = format(int(str_, 16), '032b')

        if len(str_) != 32:
            raise ValueError('Invalid Binary32 string')
        
        # 0バイト目は符号（+ or -）
        self.sign = str_[0]
        # 1〜8バイト目は指数部
        self.exp = Exponent8(str_[1:9])
        # 9〜32バイト目は仮数部
        self.fract = Fraction23(str_[9:])

    def to_f(self):
        # ゼロ
        if self.exp.to_i() == 0 and self.fract.to_f() == 0:
            return 0
        # 非正規数
        if self.exp.to_i() == 0 and self.fract.to_f() != 0:
            return float.fromhex('0x1p-126')  # Float::MIN
        # 無限大
        if self.exp.to_i() == 255 and self.fract.to_f() == 0:
            return float('inf')  # Float::INFINITY
        # NaN
        if self.exp.to_i() == 255 and self.fract.to_f() != 0:
            return float('nan')  # Float::NAN

        # 符号が0ならプラスの値、1ならマイナス
        sign = 1 if self.sign == "0" else -1
        # 仮数部を求める際に省略した1.0を戻す
        fract = self.fract.to_f() + 1
        # 指数部を求める際に足したバイアス(127)を引く
        exp = self.exp.to_i() - 127

        return sign * fract * (2 ** exp)


# 指数部の8bit
class Exponent8:
    def __init__(self, exp_str):
        self.exp = exp_str

    def to_i(self):
        return int(self.exp, 2)


# 仮数部の23bit
class Fraction23:
    def __init__(self, fract_str):
        self.fract = fract_str

    def to_f(self):
        # (b0 * 0.5) + (b1 * 0.25) + (b2 * 0.125) + (b3 * 0.0625) + ...
        return sum(int(b) * (2 ** (n * -1)) for b, n in zip(self.fract, range(1, 24)))


# 使用例
bin32_str = "52b8de3f"
bin32_str = "3fdeb852"
binary32 = Binary32(bin32_str)
print(binary32.to_f())  # 1.2000000476837158