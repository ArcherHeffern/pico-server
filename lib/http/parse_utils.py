class ParseUtils:
    @staticmethod
    def parse_key_values(s: str, pair_delim: str, kv_delim: str):
        kv = {}
        pairs = s.split(pair_delim)
        for pair in pairs:
            k, v = pair.split(kv_delim, 1)
            kv[k] = v
        return kv