import argparse
import sys

import numpy as np
from maestrowf.datastructures.core import ParameterGenerator


def process_args(args):
    n_samples = args.n
    n_dims = args.dims
    sample_type = args.sample_type
    if sample_type == "random":
        x = np.random.random((n_samples, n_dims))
    elif sample_type == "grid":
        subdivision = int(pow(n_samples, 1 / float(n_dims)))
        temp = [np.linspace(0, 1.0, subdivision) for i in range(n_dims)]
        X = np.meshgrid(*temp)
        x = np.stack([xx.flatten() for xx in X], axis=1)
    np.save(args.outfile, x)


def get_custom_generator():
    """
    Create a custom populated ParameterGenerator.

    :returns: A ParameterGenerator populated with parameters.
    """
    p_gen = ParameterGenerator()
    params = {
        "X0": {"values": [x0 for x0, x1, x2 in x], "label": "X0.%%"},
        "X1": {"values": [x1 for x0, x1, x2 in x], "label": "X1.%%"},
        "X2": {"values": [x2 for x0, x1, x2 in x], "label": "X2.%%"},
    }
    for key, value in params.items():
        p_gen.add_parameter(key, value["values"], value["label"])
    return p_gen


def setup_argparse():
    parser = argparse.ArgumentParser("Generate some samples!")
    parser.add_argument("-n", help="number of samples", default=100, type=int)
    parser.add_argument("-dims", help="number of dimensions", default=2, type=int)
    parser.add_argument(
        "-sample_type",
        help="type of sampling. options: random, grid. If grid, will try to get close to the correct number of samples",
        default="random",
    )
    parser.add_argument("-outfile", help="name of output .npy file", default="samples")
    return parser


def main():
    parser = setup_argparse()
    args = parser.parse_args()
    process_args(args)


if __name__ == "__main__":
    sys.exit(main())
