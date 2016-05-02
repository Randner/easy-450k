#!/usr/bin/env python3.5
import argparse
import os
import subprocess as sp
import yaml
import shutil
import distutils.dir_util

# define colors for fancy printing
blue_col = '\033[94m'
green_col = '\033[92m'
fail_col = '\033[91m'
endc_col = '\033[0m'
bold_col = '\033[1m'
underline_col = '\033[4m'

def setup_argparse():
    # setup command line arguments
    parser = argparse.ArgumentParser(description='Initiate a new analysis project')
    parser.add_argument('project_name', type=str, help='Desired name of a new project')
    parser.add_argument('-u',
                        '--update',
                        action='store_true',
                        help='Do not overwrite configs and data; only update script files')
    #parser.add_argument('template_name', nargs='?', type=str, default='standard')
    return parser.parse_args()

def extract_pars_from_clargs(args):
    class Parameters: pass
    pars = Parameters()

    pars.update = args.update
    pars.template_name = "illumina_450k.tmpl"
    pars.template_extension = ".tmpl"
    pars.scripts_dir_name = "Scripts"
    pars.directory_template_line = '[directories]'
    pars.project_name = args.project_name
    pars.program_dir = os.path.dirname(os.path.abspath(__file__))
    pars.working_dir = os.getcwd()
    pars.project_dir = os.path.join(pars.working_dir, args.project_name)
    pars.template_path = os.path.join(pars.program_dir, "templates", pars.template_name)
    pars.scripts_dir_path = os.path.join(pars.project_dir, pars.scripts_dir_name)

    return pars

def creating_directory_message(directory_name):
    return green_col + "  [Creating project directory]: " + blue_col + directory_name + endc_col

def creating_file_message(file_name):
    return green_col + "  [Creating file]: " + blue_col + file_name + endc_col

def section_message(section_name):
    return fail_col + section_name + endc_col

# test if the path working_dir/project_name already exists (if it's a dir or a file - doesn't matter)
def project_dir_exists(project_dir):
    if os.path.isdir(project_dir):
        return True
    return False

def load_yaml_template(pars):
    return yaml.load(open(pars.template_path))

def generate_yaml_subsection(pars, section_name):
    yaml_template = load_yaml_template(pars)
    for yaml_entry in yaml_template[section_name]:
        source = os.path.join(pars.program_dir, yaml_entry['from'])
        destination = os.path.join(pars.project_dir, yaml_entry['to'])
        if not (pars.update) or yaml_entry['overwrite_on_update']:
            yield({"source" : source, "destination" : destination})

def generate_yaml_subdirs(pars):
    yaml_template = load_yaml_template(pars)
    for directory in yaml_template['empty_dirs']:
        target_dir_path = os.path.join(pars.project_dir, directory)
        if not (pars.update and os.path.isdir(target_dir_path)):
            yield(target_dir_path)

# go through all the files in template and create a subdir for each of them
def create_subdirs(pars):
    for directory in generate_yaml_subdirs(pars):
        print(creating_directory_message(directory))
        os.mkdir(directory)

def copy_dir_trees(pars):
    for paths in generate_yaml_subsection(pars, 'file_dirs'):
        print(creating_file_message(paths["destination"]))
        distutils.dir_util.copy_tree(paths["source"], paths["destination"])

# copy other files specified in template
def copy_other_files(params):
    for paths in generate_yaml_subsection(pars, 'files'):
        print(creating_file_message(paths["destination"]))
        shutil.copyfile(paths["source"], paths["destination"])

def init_git_repo(params):
    # initialize git repo if scripts dir exists
    if os.path.isdir(pars.scripts_dir_path):
        os.chdir(pars.scripts_dir_path)
        sp.call(["git", "init"])

def create_project_dir(pars):
    if(project_dir_exists(pars.project_dir)):
        raise Exception("Cannot create project dir - already exists!")
    os.mkdir(pars.project_dir)

def template_file_exists(pars):
    return os.path.exists(pars.template_path) or os.path.isdir(pars.template_path)

def create_all(pars):
    if not pars.update:
        create_project_dir(pars)
    create_subdirs(pars)
    copy_dir_trees(pars)
    copy_other_files(pars)

if __name__=="__main__":
    args = setup_argparse()
    pars = extract_pars_from_clargs(args)

    # test if template file exists
    if not template_file_exists(pars):
        print("Template file " + pars.template_path + " does not exist or is a directory! Please specify correct template name.")
        exit(1)

    try:
        load_yaml_template(pars)
    except Exception as e:
        print("Malformed yampl template: ")
        print(e)
        exit(1)

    create_all(pars)

    if not args.update:
        try:
            pass #create_all(pars)
        except Exception as e:
            print(e)
            exit(1)
    else:
        pass
