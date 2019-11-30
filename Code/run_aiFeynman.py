import argparse
from aiFeynman import aiFeynman

parser = argparse.ArgumentParser()
parser.add_argument("--filename", type=str, help="Path to the file with the data of interest")
parser.add_argument("--maxdeg_polyfit", type=int, default=4, help="Maximum degree of the polynomial tried by the polynomial fit routine")
parser.add_argument("--err_threshold_polyfit", type=float, default=0.0001, help="Error threshold for a solution of the polynomial fit routine to be kept")
parser.add_argument("--BF_try_time", type=float, default=30, help="Time limit for each brute force code call")
parser.add_argument("--BF_error_threshold", type=float, default=0.00001, help="Error threshold for a solution of the brute force routine to be kept")
parser.add_argument("--BF_ops_file_type", type=str, default="14ops.txt", help="File containing the symbols to be used in the brute force code")
parser.add_argument("--type_of_BF", type=int, default=2, help="Parameter deciding if the brute force is looking for an additive or multiplicative factor (see paper for details)")
parser.add_argument("--first_run", type=int, default=1, help="It checks if the function call is the first one or a recursive one")
parser.add_argument("--dim_red_file", type=str, default="", help="Path to the file with the variables names and their units. If no file is passed, the variables will be assumed dimensionless and some predetermined names will be assigned to them for the found expression")
parser.add_argument("--use_MDL", type=int, default=0, help="Parameter used to turn on and off the use of the minimum description length")
parser.add_argument("--time_limit", type=float, default=36000, help="Time limit for the whole program run")
parser.add_argument("--move_dir", type=int, default=0, help="Parameter used to move the solved files to specific folders (for example results/solved")
parser.add_argument("--make_eq_vars", type=int, default=1, help="Parameter used to turn on and off making 2 variables equal")
parser.add_argument("--check_prefactor", type=int, default=1, help="Parameter used to turn on and off checking for the prefactor when using the brute force")
parser.add_argument("--NN_train_epochs", type=int, default=-1, help="Number of epochs for the training")
parser.add_argument("--err_sep_mult_factor", type=float, default=-1, help="Ratio between the error threshold for multiplicative separative check and the validation error of the neural network (see the paper for details)")
parser.add_argument("--err_sep_add_factor", type=float, default=-1, help="Ratio between the error threshold for additive separative check and the validation error of the neural network (see the paper for details)")
parser.add_argument("--err_sym_divide_factor", type=float, default=-1, help="Ratio between the error threshold for a/b symmetry check and the validation error of the neural network (see the paper for details)")
parser.add_argument("--err_sym_mult_factor", type=float, default=-1, help="Ratio between the error threshold for a*b symmetry check and the validation error of the neural network (see the paper for details)")
parser.add_argument("--err_sym_plus_factor", type=float, default=-1, help="Ratio between the error threshold for a+b symmetry check and the validation error of the neural network (see the paper for details)")
parser.add_argument("--err_sym_minus_factor", type=float, default=-1, help="Ratio between the error threshold for a-b check and the validation error of the neural network (see the paper for details)")

opts = parser.parse_args()

aiFeynman(opts.filename, maxdeg_polyfit=opts.maxdeg_polyfit, err_threshold_polyfit=opts.err_threshold_polyfit, BF_try_time=opts.BF_try_time, BF_error_threshold=opts.BF_error_threshold, BF_ops_file_type=opts.BF_ops_file_type, type_of_BF=opts.type_of_BF, first_run=opts.first_run, dim_red_file=opts.dim_red_file, use_MDL=opts.use_MDL, time_limit=opts.time_limit, move_dir=opts.move_dir, make_eq_vars=opts.make_eq_vars, check_prefactor=opts.check_prefactor, NN_train_epochs=opts.NN_train_epochs,err_sep_mult_factor=opts.err_sep_mult_factor, err_sep_add_factor=opts.err_sep_add_factor, err_sym_divide_factor=opts.err_sym_divide_factor, err_sym_mult_factor=opts.err_sym_mult_factor, err_sym_plus_factor=opts.err_sym_plus_factor, err_sym_minus_factor=opts.err_sym_minus_factor)
