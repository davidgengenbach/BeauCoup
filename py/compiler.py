"BeauCoup project, © Xiaoqi Chen @ Princeton University. License: AGPLv3"
import argparse
import json

from core import lib_compiler

parser = argparse.ArgumentParser(description="BeauCoup query compiler")
parser.add_argument("query_filename", metavar="query_filename", type=str,
                    help="Filename for the input query YAML file.")

parser.add_argument("IR_filename", metavar="IR_filename", type=str,
                    help="Filename for output Intermediate Representation JSON file.")

parser.add_argument("--gamma", type=float, default=1.0, help="Memory access limit (average # coupons per packet).")

parser.add_argument("-v","--verbose", action="store_true", help="Show additional debug info.")


args = parser.parse_args()



queries = lib_compiler.parse_file(args.query_filename, args.verbose)

qid_name_lookup = {q["qid"]:q["name"] for q in queries}

if args.gamma>1.0 or args.gamma<=0:
    raise ValueError("Illegal gamma value, should be positive and smaller than one:",args.gamma)

allocate_fn = lambda query: args.gamma/len(queries)

hash_functions = lib_compiler.generate_hash_functions(queries, allocate_fn, args.verbose)

IR = {
    "qid_name_lookup":qid_name_lookup,
    "gamma_specified":args.gamma,
    "queries":queries,
    "hash_functions":hash_functions,
}

json.dump(IR, open(args.IR_filename,"w"), indent=4)