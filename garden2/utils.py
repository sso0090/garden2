# AUTOGENERATED! DO NOT EDIT! File to edit: 01_utils.ipynb (unless otherwise specified).

__all__ = ['unpack_int64_list', 'unpack_bytes_list', 'unpack_sample', 'Reader', 'compression_code']

# Cell
import tensorflow as tf

# Cell
def unpack_int64_list(feature):
    return feature.int64_list.value

# Cell
def unpack_bytes_list(feature):
    return feature.bytes_list.value

# Cell
def unpack_sample(feats):
    return {
        'class' : unpack_int64_list(feats['class']),
        'image' : unpack_bytes_list(feats['image'])
    }

# Cell
class Reader:
    def __init__(self, fname, unpack_sample, compression=None):
        self._engine = iter(tf.compat.v1.io.tf_record_iterator(
            fname, compression_code(compression)))
        self._unpack_sample = unpack_sample

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        buffer = next(self._engine)
        example = tf.train.Example()
        example.ParseFromString(buffer)
        return self._unpack_sample(example.features.feature)

    def read_sample(self):
        try:
            return __next__(self)
        except StopIteration:
            return None

# Cell
def compression_code(compression):
    if compression is None:
        return None
    code = _tf_compression_revmap.get(compression)
    if code is None:
        raise ValueError(
            'Unknown or unsupported compression type: ' + compression)