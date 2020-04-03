import numpy as np
import os
import shutil
import subprocess
from subprocess import call
import sys
import csv
import importlib
import pandas as pd
from tqdm import tqdm
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
getBest = importlib.import_module('AI-Feynman.Code.S_multipolyfit').getBest
polyfit = importlib.import_module('AI-Feynman.Code.S_polyclean_file').polyfit
NN_sep_mult = importlib.import_module('AI-Feynman.Code.S_NN_sep_mult').NN_sep_mult
NN_sep_add = importlib.import_module('AI-Feynman.Code.S_NN_sep_add').NN_sep_add
NN_equal_vars = importlib.import_module('AI-Feynman.Code.S_NN_equal_vars').NN_equal_vars
brute_force = importlib.import_module('AI-Feynman.Code.S_brute_force').brute_force
get_inverse = importlib.import_module('AI-Feynman.Code.S_get_invers').get_inverse
get_log = importlib.import_module('AI-Feynman.Code.S_get_log').get_log
get_exp = importlib.import_module('AI-Feynman.Code.S_get_exp').get_exp
get_sin = importlib.import_module('AI-Feynman.Code.S_get_sin').get_sin
get_asin = importlib.import_module('AI-Feynman.Code.S_get_asin').get_asin
get_cos = importlib.import_module('AI-Feynman.Code.S_get_cos').get_cos
get_acos = importlib.import_module('AI-Feynman.Code.S_get_acos').get_acos
get_tan = importlib.import_module('AI-Feynman.Code.S_get_tan').get_tan
get_atan = importlib.import_module('AI-Feynman.Code.S_get_atan').get_atan
get_squared = importlib.import_module('AI-Feynman.Code.S_get_squared').get_squared
get_sqrt = importlib.import_module('AI-Feynman.Code.S_get_sqrt').get_sqrt
create_new_file_for_NN_add = importlib.import_module('AI-Feynman.Code.S_create_new_file_for_NN_add').create_new_file_for_NN_add
create_new_file_for_NN_mult = importlib.import_module('AI-Feynman.Code.S_create_new_file_for_NN_mult').create_new_file_for_NN_mult
create_new_file_for_NN_eq_vars = importlib.import_module('AI-Feynman.Code.S_create_new_file_for_NN_eq_vars').create_new_file_for_NN_eq_vars
translational_symmetry_minus = importlib.import_module('AI-Feynman.S_translational_symmetry_minus').translational_symmetry_minus
translational_symmetry_multiply = importlib.import_module('AI-Feynman.S_translational_symmetry_multiply').translational_symmetry_multiply
translational_symmetry_divide = importlib.import_module('AI-Feynman.Code.S_translational_symmetry_divide').translational_symmetry_divide
translational_symmetry_plus = importlib.import_module('AI-Feynman.Code.S_translational_symmetry_plus').gtranslational_symmetry_plus
NN_train = importlib.import_module('AI-Feynman.Code.S_NN_train').NN_train
generate_new_dimRed_xlsx_file_translation = importlib.import_module('AI-Feynman.Code.S_generate_new_dimRed_xlsx_file_translation').generate_new_dimRed_xlsx_file_translation
generate_new_dimRed_xlsx_file_equal_vars = importlib.import_module('AI-Feynman.Code.S_generate_new_dimRed_xlsx_file_equal_vars').generate_new_dimRed_xlsx_file_equal_vars
get_RMS = importlib.import_module('AI-Feynman.Code.S_get_RMS').get_RMS
create_variables_file = importlib.import_module('AI-Feynman.Code.S_get_RMS').create_variables_file

input_divide_2 = importlib.import_module('AI-Feynman.Code.S_change_input').input_divide_2
input_multiply_2 = importlib.import_module('AI-Feynman.Code.S_change_input').input_multiply_2
input_exp = importlib.import_module('AI-Feynman.Code.S_change_input').input_exp
input_log = importlib.import_module('AI-Feynman.Code.S_change_input').input_log
input_sqrt = importlib.import_module('AI-Feynman.Code.S_change_input').input_sqrt
input_squared = importlib.import_module('AI-Feynman.Code.S_change_input').input_squared
input_inverse = importlib.import_module('AI-Feynman.Code.S_change_input').input_inverse
input_sin = importlib.import_module('AI-Feynman.Code.S_change_input').input_sin
input_asin = importlib.import_module('AI-Feynman.Code.S_change_input').input_asin
input_cos = importlib.import_module('AI-Feynman.Code.S_change_input').input_cos
input_acos = importlib.import_module('AI-Feynman.Code.S_change_input').input_acos
input_tan = importlib.import_module('AI-Feynman.Code.S_change_input').input_tan
input_atan = importlib.import_module('AI-Feynman.Code.S_change_input').input_atan

try_bf_polyfit = importlib.import_module('AI-Feynman.Code.S_try_bf_polyfit').try_bf_polyfit
generate_new_dimRed_xlsx_file_transf_input = importlib.import_module('AI-Feynman.Code.S_generate_new_dimRed_xlsx_file_transf_input').generate_new_dimRed_xlsx_file_transf_input
generate_new_dimRed_xlsx_file_separable = importlib.import_module('AI-Feynman.Code.S_generate_new_dimRed_xlsx_file_separable').generate_new_dimRed_xlsx_file_separable
input_acos = importlib.import_module('AI-Feynman.Code.S_change_input').input_acos
input_tan = importlib.import_module('AI-Feynman.Code.S_change_input').input_tan
input_atan = importlib.import_module('AI-Feynman.Code.S_change_input').input_atan

try:
    os.mkdir("results/")
except:
    pass
try:
    os.mkdir("results/solved/")
except:
    pass
try:
    os.mkdir("results/solutions/")
except:
    pass
try:
    os.mkdir("results/NN_trained_models/")
except:
    pass
try:
    os.mkdir("results/NN_trained_models/models/")
except:
    pass
try:
    os.mkdir("results/equal_variables/")

except:
    pass
solved_dir = "results/solved/"


def find_formula(pathdir, filename, methods_tried, maxdeg_polyfit, err_threshold_polyfit, BF_try_time, BF_error_threshold, BF_ops_file_type, BF_sep_type, first_run, dim_red_file, use_MDL, move_dir, time_limit, make_eq_vars, check_prefactor, NN_train_epochs, err_sep_mult_factor, err_sep_add_factor, err_sym_divide_factor, err_sym_mult_factor, err_sym_plus_factor, err_sym_minus_factor):
    start_time = time.time()
    original_dir = pathdir

    try:

        # Create a file with the error threshold to be used by the mathematica code
        np.savetxt("BF_error_threshold_file.txt",[BF_error_threshold], fmt='%f')
        # Save the RMS of the output of the function
        get_RMS(pathdir,filename)

################################ NO TRANSFORM ################################
        if time.time() - start_time < time_limit:
            formula, methods_tried, not_replaced_formula = try_bf_polyfit(pathdir, filename, methods_tried, BF_try_time, BF_ops_file_type, BF_sep_type, use_MDL, check_prefactor, dim_red_file, maxdeg_polyfit, err_threshold_polyfit, first_run, move_dir, original_dir, solved_dir, "brute_force", "polyfit")
            if formula!=0:
                return (formula, methods_tried, not_replaced_formula)
        else:
            return (0, methods_tried, 0)

################################ LOG ################################
        if time.time() - start_time < time_limit:
            print("LOG")
            if first_run:
                pathdir_transf = "results/mystery_world_log/"
                get_log(pathdir,pathdir_transf,filename)
                try:
                    formula, methods_tried, not_replaced_formula = try_bf_polyfit(pathdir_transf, filename+"-log", methods_tried, BF_try_time, BF_ops_file_type, BF_sep_type, use_MDL, check_prefactor, dim_red_file, maxdeg_polyfit, err_threshold_polyfit, first_run, move_dir, original_dir, solved_dir, "brute_force_log", "polyfit_log_f")
                    if formula!=0:
                        return (exp(formula), methods_tried, exp(not_replaced_formula))
                except:
                    pass
        else:
            return (0, methods_tried, 0)
################################ INVERSE ################################
        if time.time() - start_time < time_limit:
            print("INVERSE")
            if first_run:
                pathdir_transf = "results/mystery_world_inverse/"
                get_inverse(pathdir,pathdir_transf,filename)
                try:
                    formula, methods_tried, not_replaced_formula = try_bf_polyfit(pathdir_transf, filename+"-inverse", methods_tried, BF_try_time, BF_ops_file_type, BF_sep_type, use_MDL, check_prefactor, dim_red_file, maxdeg_polyfit, err_threshold_polyfit, first_run, move_dir, original_dir, solved_dir, "brute_force_inverse", "polyfit_inverse_f")
                    if formula!=0:
                        return (1/formula, methods_tried, 1/not_replaced_formula)
                except:
                    pass
        else:
            return (0, methods_tried, 0)
################################ SQUARED ################################
        if time.time() - start_time < time_limit:
            print("SQUARED")
            if first_run:
                pathdir_transf = "results/mystery_world_squared/"
                get_squared(pathdir,pathdir_transf,filename)
                try:
                    formula, methods_tried, not_replaced_formula = try_bf_polyfit(pathdir_transf, filename+"-squared", methods_tried, BF_try_time, BF_ops_file_type, BF_sep_type, use_MDL, check_prefactor, dim_red_file, maxdeg_polyfit, err_threshold_polyfit, first_run, move_dir, original_dir, solved_dir, "brute_force_squared", "polyfit_squared_f")
                    if formula!=0:
                        return (sqrt(formula), methods_tried, sqrt(not_replaced_formula))
                except:
                    pass
        else:
            return (0, methods_tried, 0)
################################ SIN ################################
        if time.time() - start_time < time_limit:
            print("SIN")
            if first_run:
                pathdir_transf = "results/mystery_world_sin/"
                get_sin(pathdir,pathdir_transf,filename)
                try:
                    formula, methods_tried, not_replaced_formula = try_bf_polyfit(pathdir_transf, filename+"-sin", methods_tried, BF_try_time, BF_ops_file_type, BF_sep_type, use_MDL, check_prefactor, dim_red_file, maxdeg_polyfit, err_threshold_polyfit, first_run, move_dir, original_dir, solved_dir, "brute_force_sin", "polyfit_sin_f")
                    if formula!=0:
                        return (asin(formula), methods_tried, asin(not_replaced_formula))
                except:
                    pass
        else:
            return (0, methods_tried, 0)

################################ SQRT ################################
        if time.time() - start_time < time_limit:
            print("SQRT")
            if first_run:
                pathdir_transf = "results/mystery_world_sqrt/"
                get_sqrt(pathdir,pathdir_transf,filename)
                try:
                    formula, methods_tried, not_replaced_formula = try_bf_polyfit(pathdir_transf, filename+"-sqrt", methods_tried, BF_try_time, BF_ops_file_type, BF_sep_type, use_MDL, check_prefactor, dim_red_file, maxdeg_polyfit, err_threshold_polyfit, first_run, move_dir, original_dir, solved_dir, "brute_force_sqrt", "polyfit_sqrt_f")
                    if formula!=0:
                        return (formula**2, methods_tried, not_replaced_formula**2)
                except:
                    pass
        else:
            return (0, methods_tried, 0)

################################ EXP ################################
        if time.time() - start_time < time_limit:
            print("EXP")
            if first_run:
                pathdir_transf = "results/mystery_world_exp/"
                get_exp(pathdir,pathdir_transf,filename)
                try:
                    formula, methods_tried, not_replaced_formula = try_bf_polyfit(pathdir_transf, filename+"-exp", methods_tried, BF_try_time, BF_ops_file_type, BF_sep_type, use_MDL, check_prefactor, dim_red_file, maxdeg_polyfit, err_threshold_polyfit, first_run, move_dir, original_dir, solved_dir, "brute_force_exp", "polyfit_exp_f")
                    if formula!=0:
                        return (log(formula), methods_tried, log(not_replaced_formula))
                except:
                    pass

        else:
            return (0, methods_tried, 0)
################################ COS ################################
        if time.time() - start_time < time_limit:
            print("COS")
            if first_run:
                pathdir_transf = "results/mystery_world_cos/"
                get_cos(pathdir,pathdir_transf,filename)
                try:
                    formula, methods_tried, not_replaced_formula = try_bf_polyfit(pathdir_transf, filename+"-cos", methods_tried, BF_try_time, BF_ops_file_type, BF_sep_type, use_MDL, check_prefactor, dim_red_file, maxdeg_polyfit, err_threshold_polyfit, first_run, move_dir, original_dir, solved_dir, "brute_force_cos", "polyfit_cos_f")
                    if formula!=0:
                        return (acos(formula), methods_tried, acos(not_replaced_formula))
                except:
                    pass

        else:
            return (0, methods_tried, 0)
################################ ARCCOS ################################
        if time.time() - start_time < time_limit:
            print("ARCCOS")
            if first_run:
                pathdir_transf = "results/mystery_world_acos/"
                get_acos(pathdir,pathdir_transf,filename)
                try:
                    formula, methods_tried, not_replaced_formula = try_bf_polyfit(pathdir_transf, filename+"-acos", methods_tried, BF_try_time, BF_ops_file_type, BF_sep_type, use_MDL, check_prefactor, dim_red_file, maxdeg_polyfit, err_threshold_polyfit, first_run, move_dir, original_dir, solved_dir, "brute_force_acos", "polyfit_acos_f")
                    if formula!=0:
                        return (cos(formula), methods_tried, cos(not_replaced_formula))
                except:
                    pass
        else:
            return (0, methods_tried, 0)
################################ TAN ################################
        if time.time() - start_time < time_limit:
            print("TAN")
            if first_run:
                pathdir_transf = "results/mystery_world_tan/"
                get_tan(pathdir,pathdir_transf,filename)
                try:
                    formula, methods_tried, not_replaced_formula = try_bf_polyfit(pathdir_transf, filename+"-tan", methods_tried, BF_try_time, BF_ops_file_type, BF_sep_type, use_MDL, check_prefactor, dim_red_file, maxdeg_polyfit, err_threshold_polyfit, first_run, move_dir, original_dir, solved_dir, "brute_force_tan", "polyfit_tan_f")
                    if formula!=0:
                        return (atan(formula), methods_tried, atan(not_replaced_formula))
                except:
                    pass

        else:
            return (0, methods_tried, 0)
################################ ARCTAN ################################
        if time.time() - start_time < time_limit:
            print("ARCTAN")
            if first_run:
                pathdir_transf = "results/mystery_world_atan/"
                get_atan(pathdir,pathdir_transf,filename)
                try:
                    formula, methods_tried, not_replaced_formula = try_bf_polyfit(pathdir_transf, filename+"-atan", methods_tried, BF_try_time, BF_ops_file_type, BF_sep_type, use_MDL, check_prefactor, dim_red_file, maxdeg_polyfit, err_threshold_polyfit, first_run, move_dir, original_dir, solved_dir, "brute_force_atan", "polyfit_atan_f")
                    if formula!=0:
                        return (tan(formula), methods_tried, tan(not_replaced_formula))
                except:
                    pass

        else:
            return (0, methods_tried, 0)
################################ ARCSIN ################################
        if time.time() - start_time < time_limit:
            print("ARCSIN")
            if first_run:
                pathdir_transf = "results/mystery_world_asin/"
                get_asin(pathdir,pathdir_transf,filename)

                try:
                    formula, methods_tried, not_replaced_formula = try_bf_polyfit(pathdir_transf, filename+"-asin", methods_tried, BF_try_time, BF_ops_file_type, BF_sep_type, use_MDL, check_prefactor, dim_red_file, maxdeg_polyfit, err_threshold_polyfit, first_run, move_dir, original_dir, solved_dir, "brute_force_asin", "polyfit_asin_f")
                    if formula!=0:
                        return (sin(formula), methods_tried, sin(not_replaced_formula))
                except:
                    pass
        else:
            return (0, methods_tried, 0)

################################ TRANSLATIONAL SYMMETRY - - ################################
        if time.time() - start_time < time_limit:
            print("Checking for translational symmetry - -")
            methods_tried = methods_tried + ["translational_symmetry_-_-"]
            # get the indices where you can make the translational replacement
            if os.path.isfile("results/NN_trained_models/models/"+filename+".h5")==False:
                NN_train(pathdir,filename, NN_train_epochs)
            file_trans, index1, index2 = translational_symmetry_minus(pathdir,filename, err_sym_minus_factor)
            if file_trans!=0:
                print("TRANSLATIONAL SYMMETRY (-) FOUND!")
                symbol = "-"
                # create the new dimRed variables (i.e. new xlsx file)
                new_dim_red_file = generate_new_dimRed_xlsx_file_translation(dim_red_file,filename.split('-')[0],symbol,index1,index2)
                f_trans = find_formula("results/translated_data_minus/", file_trans, methods_tried, maxdeg_polyfit, err_threshold_polyfit, BF_try_time, BF_error_threshold, BF_ops_file_type, BF_sep_type, first_run, new_dim_red_file, use_MDL, 0, time_limit, make_eq_vars, check_prefactor, NN_train_epochs,err_sep_mult_factor, err_sep_add_factor, err_sym_divide_factor, err_sym_mult_factor, err_sym_plus_factor, err_sym_minus_factor)
                methods_tried = f_trans[1]
                if f_trans[0]!=0:
                    methods_tried = methods_tried + ["solved"]
                    if move_dir!=0:
                        shutil.move(original_dir+filename.split('-')[0], solved_dir)
                    return (f_trans[0], methods_tried, f_trans[2])
        else:
            return (0, methods_tried, 0)
################################ TRANSLATIONAL SYMMETRY * / ################################
        if time.time() - start_time < time_limit:
            print("Checking for translational symmetry * /")
            methods_tried = methods_tried + ["translational_symmetry_*_/"]
            if os.path.isfile("results/NN_trained_models/models/"+filename+".h5")==False:
                NN_train(pathdir,filename, NN_train_epochs)
            file_trans, index1, index2 = translational_symmetry_multiply(pathdir,filename, err_sym_mult_factor)
            if file_trans!=0:
                print("TRANSLATIONAL SYMMETRY (*) FOUND!")
                symbol = "*"
                new_dim_red_file = generate_new_dimRed_xlsx_file_translation(dim_red_file,filename.split('-')[0],symbol,index1,index2)
                f_trans = find_formula("results/translated_data_mult/", file_trans, methods_tried, maxdeg_polyfit, err_threshold_polyfit, BF_try_time, BF_error_threshold, BF_ops_file_type, BF_sep_type, first_run, new_dim_red_file, use_MDL, 0, time_limit, make_eq_vars, check_prefactor, NN_train_epochs,err_sep_mult_factor, err_sep_add_factor, err_sym_divide_factor, err_sym_mult_factor, err_sym_plus_factor, err_sym_minus_factor)
                methods_tried = f_trans[1]
                if f_trans[0]!=0:
                    methods_tried = methods_tried + ["solved"]
                    if move_dir!=0:
                        shutil.move(original_dir+filename.split('-')[0], solved_dir)
                    return (f_trans[0], methods_tried,f_trans[2])
        else:
            return (0, methods_tried, 0)
################################ TRANSLATIONAL SYMMETRY * * ################################
        if time.time() - start_time < time_limit:
            print("Checking for translational symmetry * *")
            methods_tried = methods_tried + ["translational_symmetry_*_*"]
            if os.path.isfile("results/NN_trained_models/models/"+filename+".h5")==False:
                NN_train(pathdir,filename, NN_train_epochs)
            file_trans, index1, index2 = translational_symmetry_divide(pathdir,filename,err_sym_divide_factor)
            if file_trans!=0:
                print("TRANSLATIONAL SYMMETRY (/) FOUND!")
                symbol = "/"
                new_dim_red_file = generate_new_dimRed_xlsx_file_translation(dim_red_file,filename.split('-')[0],symbol,index1,index2)
                f_trans = find_formula("results/translated_data_divide/", file_trans, methods_tried, maxdeg_polyfit, err_threshold_polyfit, BF_try_time, BF_error_threshold, BF_ops_file_type, BF_sep_type, first_run, new_dim_red_file, use_MDL, 0, time_limit, make_eq_vars, check_prefactor, NN_train_epochs,err_sep_mult_factor, err_sep_add_factor, err_sym_divide_factor, err_sym_mult_factor, err_sym_plus_factor, err_sym_minus_factor)
                methods_tried = f_trans[1]
                if f_trans[0]!=0:
                    methods_tried = methods_tried + ["solved"]
                    if move_dir!=0:
                        shutil.move(original_dir+filename.split('-')[0], solved_dir)
                    return (f_trans[0], methods_tried,f_trans[2])
        else:
            return (0, methods_tried, 0)
################################ TRANSLATIONAL SYMMETRY + - ################################
        if time.time() - start_time < time_limit:
            print("Checking for translational symmetry + -")
            methods_tried = methods_tried + ["translational_symmetry_+_-"]
            # get the indices where you can make the translational replacement
            if os.path.isfile("results/NN_trained_models/models/"+filename+".h5")==False:
                NN_train(pathdir,filename, NN_train_epochs)
            file_trans, index1, index2 = translational_symmetry_plus(pathdir,filename, err_sym_plus_factor)
            if file_trans!=0:
                print("TRANSLATIONAL SYMMETRY (+) FOUND!")
                symbol = "+"
                # create the new dimRed variables (i.e. new xlsx file)
                new_dim_red_file = generate_new_dimRed_xlsx_file_translation(dim_red_file,filename.split('-')[0],symbol,index1,index2)
                f_trans = find_formula("results/translated_data_plus/", file_trans, methods_tried, maxdeg_polyfit, err_threshold_polyfit, BF_try_time, BF_error_threshold, BF_ops_file_type, BF_sep_type, first_run, new_dim_red_file, use_MDL, 0, time_limit, make_eq_vars, check_prefactor, NN_train_epochs,err_sep_mult_factor, err_sep_add_factor, err_sym_divide_factor, err_sym_mult_factor, err_sym_plus_factor, err_sym_minus_factor)
                methods_tried = f_trans[1]
                if f_trans[0]!=0:
                    methods_tried = methods_tried + ["solved"]
                    if move_dir!=0:
                        shutil.move(original_dir+filename.split('-')[0], solved_dir)
                    return (f_trans[0], methods_tried, f_trans[2])
        else:
            return (0, methods_tried, 0)


################################ MULT SEPARABILITY ################################
        if time.time() - start_time < time_limit:
            # Check for multiplicative separability
            print("Checking for multiplicative separability")
            methods_tried = methods_tried + ["separate_mult"]
            if os.path.isfile("results/NN_trained_models/models/"+filename+".h5")==False:
                NN_train(pathdir,filename, NN_train_epochs)
            file_sep_m_1, file_sep_m_2, indices_1, indices_2 = NN_sep_mult(pathdir,filename, err_sym_mult_factor)
            # if separable I should get filenames here, not zeros
            if file_sep_m_1!=0 and file_sep_m_2!=0:
                print("SEPARABLE MULT!!!!!!!!!!")
                # create the new xlsx file with just the needed indices (indices_2 - says which ones to remove)
                NN_error = NN_eval(pathdir,filename).data.cpu()
                print("mult error: ", NN_error)
                new_dim_red_file_separable = generate_new_dimRed_xlsx_file_separable(dim_red_file,filename.split('-')[0],indices_2, "left")
                f_s_m_1 = find_formula("results/separable_mult/", file_sep_m_1, methods_tried, maxdeg_polyfit, 10*NN_error, BF_try_time, 300*NN_error, BF_ops_file_type, 2, 0, new_dim_red_file_separable, 1, 0, time_limit, make_eq_vars, 0, NN_train_epochs,err_sep_mult_factor, err_sep_add_factor, err_sym_divide_factor, err_sym_mult_factor, err_sym_plus_factor, err_sym_minus_factor)
                methods_tried = f_s_m_1[1]
                #check if the first file has a non-zero output (without the constant term)
                if f_s_m_1[0]!=0:
                    new_NN_mult_file = create_new_file_for_NN_mult(pathdir,filename,filename+"-sep_mult",indices_1,f_s_m_1[2])
                    new_dim_red_file_separable = generate_new_dimRed_xlsx_file_separable(dim_red_file,filename.split('-')[0],indices_1, "right")
                    new_f_s_m_1 = find_formula(pathdir, new_NN_mult_file, methods_tried, maxdeg_polyfit, err_threshold_polyfit, BF_try_time, BF_error_threshold, BF_ops_file_type, BF_sep_type, first_run, new_dim_red_file_separable, use_MDL, 0, time_limit, make_eq_vars, check_prefactor, NN_train_epochs,err_sep_mult_factor, err_sep_add_factor, err_sym_divide_factor, err_sym_mult_factor, err_sym_plus_factor, err_sym_minus_factor)
                    methods_tried = new_f_s_m_1[1]
                    # if the second part is not 0, return the sum of the 2
                    if new_f_s_m_1[0]!=0:
                        methods_tried = methods_tried + ["solved"]
                        if move_dir!=0:
                            shutil.move(original_dir+filename.split('-')[0], solved_dir)
                        return(f_s_m_1[0]*new_f_s_m_1[0],methods_tried,f_s_m_1[0]*new_f_s_m_1[0]) # temporary solution
            print("Multiplicative separability not found")
        else:
            return (0, methods_tried, 0)

################################ ADD SEPARABILITY ################################
        if time.time() - start_time < time_limit:
            # Check for additive separability
            # e.g. sin(alpha)+cos(beta)*gamma**2
            print("Checking for additive separability")
            methods_tried = methods_tried + ["separate_add"]
            if os.path.isfile("results/NN_trained_models/models/"+filename+".h5")==False:
                NN_train(pathdir,filename, NN_train_epochs)
            file_sep_a_1, file_sep_a_2, indices_1, indices_2 = NN_sep_add(pathdir,filename,err_sep_add_factor)
            # if separable I should get filenames here, not zeros
            if file_sep_a_1!=0 and file_sep_a_2!=0:
                print("SEPARABLE ADD!!!!!!!!!!")
                # create the new xlsx file with just the needed indices (indices_2 - says which ones to remove)
                NN_error = NN_eval(pathdir,filename).data.cpu()
                new_dim_red_file_separable = generate_new_dimRed_xlsx_file_separable(dim_red_file,filename.split('-')[0],indices_2, "left")
                f_s_a_1 = find_formula("results/separable_add/", file_sep_a_1, methods_tried, maxdeg_polyfit, 10*NN_error, BF_try_time, 300*NN_error, BF_ops_file_type, 3, 0, new_dim_red_file_separable, 1, 0, time_limit, make_eq_vars, 0, NN_train_epochs,err_sep_mult_factor, err_sep_add_factor, err_sym_divide_factor, err_sym_mult_factor, err_sym_plus_factor, err_sym_minus_factor)
                methods_tried = f_s_a_1[1]
                #check if the first file has a non-zero output (without the constant term): sin(alpha)
                if f_s_a_1[0]!=0:
                    print("CREATE A NEW FILE!")
                    new_NN_add_file = create_new_file_for_NN_add(pathdir,filename,filename+"-sep_add",indices_1,f_s_a_1[2])
                    # get recursively the other part of the equation (the first one is f_s_a_1, the second one is new_f_s_a_1)
                    new_dim_red_file_separable = generate_new_dimRed_xlsx_file_separable(dim_red_file,filename.split('-')[0],indices_1, "right")
                    new_f_s_a_1 = find_formula(pathdir, new_NN_add_file, methods_tried, maxdeg_polyfit, err_threshold_polyfit, BF_try_time, BF_error_threshold, BF_ops_file_type, BF_sep_type, first_run, new_dim_red_file_separable, use_MDL, 0, time_limit, make_eq_vars, check_prefactor, NN_train_epochs,err_sep_mult_factor, err_sep_add_factor, err_sym_divide_factor, err_sym_mult_factor, err_sym_plus_factor, err_sym_minus_factor)
                    methods_tried = new_f_s_a_1[1]
                    # if the second part is not 0, return the sum of the 2
                    if new_f_s_a_1[2]!=0:
                        methods_tried = methods_tried + ["solved"]
                        if move_dir!=0:
                            shutil.move(original_dir+filename.split('-')[0], solved_dir)
                        return(f_s_a_1[0]+new_f_s_a_1[0],methods_tried,f_s_a_1[0]+new_f_s_a_1[0]) # temporary solution

        else:
            return (0, methods_tried, 0)

################################ EQUAL VARIABLES ################################
        if time.time() - start_time < time_limit:
            if first_run and make_eq_vars:
                # Check what happens when 2 variables are equal
                print("Making 2 variables equal")
                methods_tried = methods_tried + ["equal_variables"]
                n_variables = np.loadtxt(pathdir+filename, dtype='str').shape[1]-1

                NN_error = NN_eval(pathdir,filename).data.cpu()
                if NN_error<0.01:
                    for i_idx in range(n_variables):
                        for j_idx in range(n_variables):
                            if i_idx<j_idx:
                                if os.path.isfile("results/NN_trained_models/models/"+filename+".h5")==False:
                                    NN_train(pathdir,filename, NN_train_epochs)
                                files = NN_equal_vars(pathdir,filename,i_idx,j_idx)
                                # generate the new xlsx file
                                new_dim_red_file_eq_vars = generate_new_dimRed_xlsx_file_equal_vars(dim_red_file,filename.split('-')[0],j_idx)
                                # try to find the formula for the equation when 2 variables are equal (this uses NN output) - use MDL here
                                fs_1 = find_formula("results/equal_variables/", files, methods_tried, maxdeg_polyfit, 10*NN_error, BF_try_time, 300*NN_error, BF_ops_file_type, 2, 0, new_dim_red_file_eq_vars, 1, 0, time_limit, 0, check_prefactor, NN_train_epochs,err_sep_mult_factor, err_sep_add_factor, err_sym_divide_factor, err_sym_mult_factor, err_sym_plus_factor, err_sym_minus_factor)
                                methods_tried = fs_1[1]
                                if fs_1[0]!=0:
                                    # get the newly created file by dividing f(a,b)/f(a,a)
                                    new_eq_var_file = create_new_file_for_NN_eq_vars(pathdir,filename,filename+"-eq_vars",i_idx,fs_1[2])
                                    # try to find the formula for the equation for f(a,b)/f(a,a) (this DOESN'T use NN output)

                                    ################### REPLACE THE 300 WITH BF_try_time !!!!!!! THIS IS JUST FOR TESTING PURPOSES
                                    fs_2 = find_formula(pathdir, new_eq_var_file, methods_tried, maxdeg_polyfit, err_threshold_polyfit, 300, BF_error_threshold, BF_ops_file_type, BF_sep_type, first_run, dim_red_file, use_MDL, 0, time_limit, 0, check_prefactor, NN_train_epochs,err_sep_mult_factor, err_sep_add_factor, err_sym_divide_factor, err_sym_mult_factor, err_sym_plus_factor, err_sym_minus_factor)
                                    methods_tried = fs_2[1]
                                    if fs_2[0]!=0:
                                        methods_tried = methods_tried + ["solved"]
                                        if move_dir!=0:
                                            shutil.move(original_dir+filename.split('-')[0], solved_dir)
                                        return (fs_1[0]*fs_2[0], methods_tried, fs_1[2]*fs_2[2])

        else:
            return (0, methods_tried, 0)

################################ DIVIDE INPUT BY 2 ################################
        if time.time() - start_time < time_limit:
            print("Divide input variables by 2!")
            n_variables = np.loadtxt(pathdir+filename, dtype='str').shape[1]-1
            pathdir_transf = "results/mystery_world_input_divide_2/"
            for i_idx in range(n_variables):
                file_name_div_2 = input_divide_2(pathdir,filename,i_idx)
                new_dim_red_file_div_inp_2 = generate_new_dimRed_xlsx_file_transf_input(dim_red_file,filename.split('-')[0],i_idx, "div2")
                try:
                    formula, methods_tried, not_replaced_formula = try_bf_polyfit(pathdir_transf, file_name_div_2, methods_tried, BF_try_time, BF_ops_file_type, BF_sep_type, use_MDL, check_prefactor, new_dim_red_file_div_inp_2, maxdeg_polyfit, err_threshold_polyfit, first_run, move_dir, original_dir, solved_dir, "bf_divide_input_by_2", "polyfit_divide_input_by_2")
                    if formula!=0:
                        return (formula, methods_tried, not_replaced_formula)
                except:
                    pass
        else:
            return (0, methods_tried, 0)


################################ MULTIPLY INPUT BY 2 ################################
        if time.time() - start_time < time_limit:
            if first_run:
                print("Multiply input variables by 2!")
                methods_tried = methods_tried + ["multiply_input_by_2"]
                n_variables = np.loadtxt(pathdir+filename, dtype='str').shape[1]-1

                for i_idx in range(n_variables):
                    file_name_mult_2 = input_multiply_2(pathdir,filename,i_idx)
                    new_dim_red_file_mult_inp_2 = generate_new_dimRed_xlsx_file_transf_input(dim_red_file,filename.split('-')[0],i_idx, "mult2")
                    f_nm_mult_2 = find_formula("results/mystery_world_input_multiply_2/", file_name_mult_2, methods_tried, maxdeg_polyfit, err_threshold_polyfit, BF_try_time, BF_error_threshold, BF_ops_file_type, BF_sep_type, 0, new_dim_red_file_mult_inp_2, use_MDL, 0, time_limit, 0, check_prefactor, NN_train_epochs,err_sep_mult_factor, err_sep_add_factor, err_sym_divide_factor, err_sym_mult_factor, err_sym_plus_factor, err_sym_minus_factor)
                    methods_tried = f_nm_mult_2[1]
                    if f_nm_mult_2[0]!=0:
                        methods_tried = methods_tried + ["solved"]
                        if move_dir!=0:
                            shutil.move(original_dir+filename.split('-')[0], solved_dir)
                        return(f_nm_mult_2[0],methods_tried,f_nm_mult_2[2])
        else:
            return (0, methods_tried, 0)

################################ EXP INPUT ################################
        if time.time() - start_time < time_limit:
            if first_run:
                methods_tried = methods_tried + ["exp_input"]
                n_variables = np.loadtxt(pathdir+filename, dtype='str').shape[1]-1

                for i_idx in range(n_variables):
                    file_name_exp = input_exp(pathdir,filename,i_idx)
                    new_dim_red_file_exp = generate_new_dimRed_xlsx_file_transf_input(dim_red_file,filename.split('-')[0],i_idx, "exp")
                    f_nm_exp = find_formula("results/mystery_world_input_exp/", file_name_exp, methods_tried, maxdeg_polyfit, err_threshold_polyfit, BF_try_time, BF_error_threshold, BF_ops_file_type, BF_sep_type, 0, new_dim_red_file_exp, use_MDL, 0, time_limit, 0, check_prefactor, NN_train_epochs,err_sep_mult_factor, err_sep_add_factor, err_sym_divide_factor, err_sym_mult_factor, err_sym_plus_factor, err_sym_minus_factor)
                    methods_tried = f_nm_exp[1]
                    if f_nm_exp[0]!=0:
                        methods_tried = methods_tried + ["solved"]
                        if move_dir!=0:
                            shutil.move(original_dir+filename.split('-')[0], solved_dir)
                        return(f_nm_exp[0],methods_tried,f_nm_exp[2])
        else:
            return (0, methods_tried, 0)
################################ LOG INPUT ################################
        if time.time() - start_time < time_limit:
            if first_run:
                print("Log input variables")
                methods_tried = methods_tried + ["log_input"]
                n_variables = np.loadtxt(pathdir+filename, dtype='str').shape[1]-1

                for i_idx in range(n_variables):
                    file_name_log = input_log(pathdir,filename,i_idx)
                    new_dim_red_file_log = generate_new_dimRed_xlsx_file_transf_input(dim_red_file,filename.split('-')[0],i_idx, "log")
                    f_nm_log = find_formula("results/mystery_world_input_log/", file_name_log, methods_tried, maxdeg_polyfit, err_threshold_polyfit, BF_try_time, BF_error_threshold, BF_ops_file_type, BF_sep_type, 0, new_dim_red_file_log, use_MDL, 0, time_limit, 0, check_prefactor, NN_train_epochs,err_sep_mult_factor, err_sep_add_factor, err_sym_divide_factor, err_sym_mult_factor, err_sym_plus_factor, err_sym_minus_factor)
                    methods_tried = f_nm_log[1]
                    if f_nm_log[0]!=0:
                        methods_tried = methods_tried + ["solved"]
                        if move_dir!=0:
                            shutil.move(original_dir+filename.split('-')[0], solved_dir)
                        return(f_nm_log[0],methods_tried,f_nm_log[2])
        else:
            return (0, methods_tried, 0)

################################ SQRT INPUT ################################
        if time.time() - start_time < time_limit:
            if first_run:
                print("Sqrt input variables")
                methods_tried = methods_tried + ["sqrt_input"]
                n_variables = np.loadtxt(pathdir+filename, dtype='str').shape[1]-1

                for i_idx in range(n_variables):
                    file_name_sqrt = input_sqrt(pathdir,filename,i_idx)
                    new_dim_red_file_sqrt = generate_new_dimRed_xlsx_file_transf_input(dim_red_file,filename.split('-')[0],i_idx, "sqrt")
                    f_nm_sqrt = find_formula("results/mystery_world_input_sqrt/", file_name_sqrt, methods_tried, maxdeg_polyfit, err_threshold_polyfit, BF_try_time, BF_error_threshold, BF_ops_file_type, BF_sep_type, 0, new_dim_red_file_sqrt, use_MDL, 0, time_limit, 0, check_prefactor, NN_train_epochs,err_sep_mult_factor, err_sep_add_factor, err_sym_divide_factor, err_sym_mult_factor, err_sym_plus_factor, err_sym_minus_factor)
                    methods_tried = f_nm_sqrt[1]
                    if f_nm_sqrt[0]!=0:
                        methods_tried = methods_tried + ["solved"]
                        if move_dir!=0:
                            shutil.move(original_dir+filename.split('-')[0], solved_dir)
                        return(f_nm_sqrt[0],methods_tried,f_nm_sqrt[2])
        else:
            return (0, methods_tried, 0)

################################ SQUARED INPUT ################################
        if time.time() - start_time < time_limit:
            if first_run:
                print("Squared input variables")
                methods_tried = methods_tried + ["squared_input"]
                n_variables = np.loadtxt(pathdir+filename, dtype='str').shape[1]-1

                for i_idx in range(n_variables):
                    file_name_squared = input_squared(pathdir,filename,i_idx)
                    new_dim_red_file_squared = generate_new_dimRed_xlsx_file_transf_input(dim_red_file,filename.split('-')[0],i_idx, "squared")
                    f_nm_squared = find_formula("results/mystery_world_input_squared/", file_name_squared, methods_tried, maxdeg_polyfit, err_threshold_polyfit, BF_try_time, BF_error_threshold, BF_ops_file_type, BF_sep_type, 0, new_dim_red_file_squared, use_MDL, 0, time_limit, 0, check_prefactor, NN_train_epochs,err_sep_mult_factor, err_sep_add_factor, err_sym_divide_factor, err_sym_mult_factor, err_sym_plus_factor, err_sym_minus_factor)
                    methods_tried = f_nm_squared[1]
                    if f_nm_squared[0]!=0:
                        methods_tried = methods_tried + ["solved"]
                        if move_dir!=0:
                            shutil.move(original_dir+filename.split('-')[0], solved_dir)
                        return(f_nm_squared[0],methods_tried,f_nm_squared[2])
        else:
            return (0, methods_tried, 0)

################################ INVERSE INPUT ################################
        if time.time() - start_time < time_limit:
            if first_run:
                print("Inverse input variables")
                methods_tried = methods_tried + ["inverse_input"]
                n_variables = np.loadtxt(pathdir+filename, dtype='str').shape[1]-1

                for i_idx in range(n_variables):
                    file_name_inverse = input_inverse(pathdir,filename,i_idx)
                    new_dim_red_file_inverse = generate_new_dimRed_xlsx_file_transf_input(dim_red_file,filename.split('-')[0],i_idx, "inverse")
                    f_nm_inverse = find_formula("results/mystery_world_input_inverse/", file_name_inverse, methods_tried, maxdeg_polyfit, err_threshold_polyfit, BF_try_time, BF_error_threshold, BF_ops_file_type, BF_sep_type, 0, new_dim_red_file_inverse, use_MDL, 0, time_limit, 0, check_prefactor, NN_train_epochs,err_sep_mult_factor, err_sep_add_factor, err_sym_divide_factor, err_sym_mult_factor, err_sym_plus_factor, err_sym_minus_factor)
                    methods_tried = f_nm_inverse[1]
                    if f_nm_inverse[0]!=0:
                        methods_tried = methods_tried + ["solved"]
                        if move_dir!=0:
                            shutil.move(original_dir+filename.split('-')[0], solved_dir)
                        return(f_nm_inverse[0],methods_tried,f_nm_inverse[2])
        else:
            return (0, methods_tried, 0)

################################ SIN INPUT ################################
        if time.time() - start_time < time_limit:
            if first_run:
                print("Sin input variables")
                methods_tried = methods_tried + ["sin_input"]
                n_variables = np.loadtxt(pathdir+filename, dtype='str').shape[1]-1

                for i_idx in range(n_variables):
                    file_name_sin = input_sin(pathdir,filename,i_idx)
                    new_dim_red_file_sin = generate_new_dimRed_xlsx_file_transf_input(dim_red_file,filename.split('-')[0],i_idx, "sin")
                    f_nm_sin = find_formula("results/mystery_world_input_sin/", file_name_sin, methods_tried, maxdeg_polyfit, err_threshold_polyfit, BF_try_time, BF_error_threshold, BF_ops_file_type, BF_sep_type, 0, new_dim_red_file_sin, use_MDL, 0, time_limit, 0, check_prefactor, NN_train_epochs,err_sep_mult_factor, err_sep_add_factor, err_sym_divide_factor, err_sym_mult_factor, err_sym_plus_factor, err_sym_minus_factor)
                    methods_tried = f_nm_sin[1]
                    if f_nm_sin[0]!=0:
                        methods_tried = methods_tried + ["solved"]
                        if move_dir!=0:
                            shutil.move(original_dir+filename.split('-')[0], solved_dir)
                        return(f_nm_sin[0],methods_tried,f_nm_sin[2])
        else:
            return (0, methods_tried, 0)

################################ ASIN INPUT ################################
        if time.time() - start_time < time_limit:
            if first_run:
                print("Arcsin input variables")
                methods_tried = methods_tried + ["asin_input"]
                n_variables = np.loadtxt(pathdir+filename, dtype='str').shape[1]-1

                for i_idx in range(n_variables):
                    file_name_asin = input_asin(pathdir,filename,i_idx)
                    new_dim_red_file_asin = generate_new_dimRed_xlsx_file_transf_input(dim_red_file,filename.split('-')[0],i_idx, "asin")
                    f_nm_asin = find_formula("results/mystery_world_input_asin/", file_name_asin, methods_tried, maxdeg_polyfit, err_threshold_polyfit, BF_try_time, BF_error_threshold, BF_ops_file_type, BF_sep_type, 0, new_dim_red_file_asin, use_MDL, 0, time_limit, 0, check_prefactor, NN_train_epochs,err_sep_mult_factor, err_sep_add_factor, err_sym_divide_factor, err_sym_mult_factor, err_sym_plus_factor, err_sym_minus_factor)
                    methods_tried = f_nm_asin[1]
                    if f_nm_asin[0]!=0:
                        methods_tried = methods_tried + ["solved"]
                        if move_dir!=0:
                            shutil.move(original_dir+filename.split('-')[0], solved_dir)
                        return(f_nm_asin[0],methods_tried,f_nm_asin[2])
        else:
            return (0, methods_tried, 0)

################################ COS INPUT ################################
        if time.time() - start_time < time_limit:
            if first_run:
                print("Cos input variables")
                methods_tried = methods_tried + ["cos_input"]
                n_variables = np.loadtxt(pathdir+filename, dtype='str').shape[1]-1

                for i_idx in range(n_variables):
                    file_name_cos = input_cos(pathdir,filename,i_idx)
                    new_dim_red_file_cos = generate_new_dimRed_xlsx_file_transf_input(dim_red_file,filename.split('-')[0],i_idx, "cos")
                    f_nm_cos = find_formula("results/mystery_world_input_cos/", file_name_cos, methods_tried, maxdeg_polyfit, err_threshold_polyfit, BF_try_time, BF_error_threshold, BF_ops_file_type, BF_sep_type, 0, new_dim_red_file_cos, use_MDL, 0, time_limit, 0, check_prefactor, NN_train_epochs,err_sep_mult_factor, err_sep_add_factor, err_sym_divide_factor, err_sym_mult_factor, err_sym_plus_factor, err_sym_minus_factor)
                    methods_tried = f_nm_cos[1]
                    if f_nm_cos[0]!=0:
                        methods_tried = methods_tried + ["solved"]
                        if move_dir!=0:
                            shutil.move(original_dir+filename.split('-')[0], solved_dir)
                        return(f_nm_cos[0],methods_tried,f_nm_cos[2])
        else:
            return (0, methods_tried, 0)

################################ ACOS INPUT ################################
        if time.time() - start_time < time_limit:
            if first_run:
                print("Arccos input variables")
                methods_tried = methods_tried + ["acos_input"]
                n_variables = np.loadtxt(pathdir+filename, dtype='str').shape[1]-1

                for i_idx in range(n_variables):
                    file_name_acos = input_acos(pathdir,filename,i_idx)
                    new_dim_red_file_acos = generate_new_dimRed_xlsx_file_transf_input(dim_red_file,filename.split('-')[0],i_idx, "acos")
                    f_nm_acos = find_formula("results/mystery_world_input_acos/", file_name_acos, methods_tried, maxdeg_polyfit, err_threshold_polyfit, BF_try_time, BF_error_threshold, BF_ops_file_type, BF_sep_type, 0, new_dim_red_file_acos, use_MDL, 0, time_limit, 0, check_prefactor, NN_train_epochs,err_sep_mult_factor, err_sep_add_factor, err_sym_divide_factor, err_sym_mult_factor, err_sym_plus_factor, err_sym_minus_factor)
                    methods_tried = f_nm_acos[1]
                    if f_nm_acos[0]!=0:
                        methods_tried = methods_tried + ["solved"]
                        if move_dir!=0:
                            shutil.move(original_dir+filename.split('-')[0], solved_dir)
                        return(f_nm_acos[0],methods_tried,f_nm_acos[2])
        else:
            return (0, methods_tried, 0)

################################ TAN INPUT ################################
        if time.time() - start_time < time_limit:
            if first_run:
                print("Tan input variables")
                methods_tried = methods_tried + ["tan_input"]
                n_variables = np.loadtxt(pathdir+filename, dtype='str').shape[1]-1

                for i_idx in range(n_variables):
                    file_name_tan = input_tan(pathdir,filename,i_idx)
                    new_dim_red_file_tan = generate_new_dimRed_xlsx_file_transf_input(dim_red_file,filename.split('-')[0],i_idx, "tan")
                    f_nm_tan = find_formula("results/mystery_world_input_tan/", file_name_tan, methods_tried, maxdeg_polyfit, err_threshold_polyfit, BF_try_time, BF_error_threshold, BF_ops_file_type, BF_sep_type, 0, new_dim_red_file_tan, use_MDL, 0, time_limit, 0, check_prefactor, NN_train_epochs,err_sep_mult_factor, err_sep_add_factor, err_sym_divide_factor, err_sym_mult_factor, err_sym_plus_factor, err_sym_minus_factor)
                    methods_tried = f_nm_tan[1]
                    if f_nm_tan[0]!=0:
                        methods_tried = methods_tried + ["solved"]
                        if move_dir!=0:
                            shutil.move(original_dir+filename.split('-')[0], solved_dir)
                        return(f_nm_tan[0],methods_tried,f_nm_tan[2])
        else:
            return (0, methods_tried, 0)

################################ ATAN INPUT ################################
        if time.time() - start_time < time_limit:
            if first_run:
                print("Arctan input variables")
                methods_tried = methods_tried + ["atan_input"]
                n_variables = np.loadtxt(pathdir+filename, dtype='str').shape[1]-1

                for i_idx in range(n_variables):
                    file_name_atan = input_atan(pathdir,filename,i_idx)
                    new_dim_red_file_atan = generate_new_dimRed_xlsx_file_transf_input(dim_red_file,filename.split('-')[0],i_idx, "atan")
                    f_nm_atan = find_formula("results/mystery_world_input_atan/", file_name_atan, methods_tried, maxdeg_polyfit, err_threshold_polyfit, BF_try_time, BF_error_threshold, BF_ops_file_type, BF_sep_type, 0, new_dim_red_file_atan, use_MDL, 0, time_limit, 0, check_prefactor, NN_train_epochs,err_sep_mult_factor, err_sep_add_factor, err_sym_divide_factor, err_sym_mult_factor, err_sym_plus_factor, err_sym_minus_factor)
                    methods_tried = f_nm_atan[1]
                    if f_nm_atan[0]!=0:
                        methods_tried = methods_tried + ["solved"]
                        if move_dir!=0:
                            shutil.move(original_dir+filename.split('-')[0], solved_dir)
                        return(f_nm_atan[0],methods_tried,f_nm_atan[2])
        else:
            return (0, methods_tried, 0)

    except Exception as e:
        print(e)
        return (0, methods_tried,0)

    return (0, methods_tried, 0)


################################ MAIN PROGRAM ################################

def aiFeynman(pathdir, maxdeg_polyfit=4, err_threshold_polyfit=0.0001, BF_try_time=60, BF_error_threshold=0.00001, BF_ops_file_type="14ops.txt", type_of_BF=2, first_run=1, dim_red_file="", use_MDL=0, time_limit=3600, move_dir=0, make_eq_vars=1, check_prefactor=1,NN_train_epochs=-1,err_sep_mult_factor=-1, err_sep_add_factor=-1, err_sym_divide_factor=-1, err_sym_mult_factor=-1, err_sym_plus_factor=-1, err_sym_minus_factor=-1):

    # separate the name of the file and the name of the directory
    fn_list = [pathdir[pathdir.rfind('/')+1:]]
    pathdir = pathdir[0:pathdir.rfind('/')+1]

    nn_vars = np.loadtxt(pathdir+fn_list[0], dtype='str').shape[1]-1
    # create a variables file, if dim_red_file=""
    if dim_red_file=="":
        dim_red_file = create_variables_file(nn_vars,fn_list[0])

    original_dir = pathdir
    formulas_solved_part = pd.read_excel(dim_red_file)["Formula"]
    filename_solved_part = pd.read_excel(dim_red_file)["Filename"]

    for filename in fn_list:
        try:
            print(filename)
            methods_tried = ["dim_analysis"]
            # file to write the solution
            file_exist = 0
            if (os.path.exists(pathdir+filename)):
                file_exist = 1
                solved_file = open("results/solutions/" + filename + ".txt","w")

################################ DIMENSIONAL ANALYSIS ################################
            # Check if it got solved by dimensional analysis
            dim_check = open(pathdir+filename, "r").readlines()
            if(len(dim_check[0].split())==1):
                methods_tried = methods_tried + ["solved"]
                shutil.move(original_dir+filename.split('-')[0], solved_dir)
                solved_file.write(filename)
                solved_file.write(" ")
                for k in range(len(filename_solved_part)):
                    if filename_solved_part[k]==filename:
                        solved_file.write(str(parse_expr(str(np.round(float(dim_check[0].split()[0]),3)))*parse_expr(formulas_solved_part[k])))
                solved_file.write(" ")
                solved_file.write(str(methods_tried))
                solved_file.write("\n")
                continue

            translational_operations = [] # use this to keep track of the translational operations. The format should be ["*",i,j,"-",k,l]
            # check if the formula was found at all and save it to file
            start_time = time.time()

            formula, methods_tried, _,  = find_formula(pathdir, filename, methods_tried, maxdeg_polyfit, err_threshold_polyfit, BF_try_time,BF_error_threshold, BF_ops_file_type, type_of_BF, first_run, dim_red_file, use_MDL, move_dir, time_limit, make_eq_vars, check_prefactor,NN_train_epochs,err_sep_mult_factor, err_sep_add_factor, err_sym_divide_factor, err_sym_mult_factor, err_sym_plus_factor, err_sym_minus_factor)


            print("FORMULA: ", formula)
            if formula!=0:
                solved_file.write(filename)
                solved_file.write(" ")
                for k in range(len(filename_solved_part)):
                    if filename_solved_part[k]==filename:
                        if formulas_solved_part[k]==" " or formulas_solved_part[k]==1 or formulas_solved_part[k]=="" or np.isnan(formulas_solved_part[k]):
                            solved_file.write(str(formula))
                        else:
                            print("Saved to file!!!!!")
                            print(formula)
                            print(formulas_solved_part[k])
                            solved_file.write(str(simplify(formula*parse_expr(formulas_solved_part[k]))))
                            print("Saved to file!!!!!")
                solved_file.write(" ")
                print("METHODS: ", methods_tried)
                solved_file.write(str(methods_tried))
                solved_file.write(" ")
                solved_file.write(str(time.time() - start_time))
                print("Saved to file!!!!!")
                solved_file.write("\n")
            else:
                continue

            if file_exist==1:
                solved_file.close()

        except Exception as e:
            print(e)
            continue





