"""
simply reads the byparms file and outputs a text file with the salient information.

execute the parse_byparms_df(), or execute()
"""


# import os
import custom_tools
import pandas as pd
import re
import tkinter as tk


class gui():
    def __init__(self):
        top = tk.Tk()
        top.title = 'Extract Byonic parameters'

        b = tk.Button(top, text='Click to run extract byonic parameters', command=self.button_extract_byparms)
        b.pack(pady=10)

        top.mainloop()

    def button_extract_byparms(self):
        get_text_from_byparms_file()



def get_text_from_byparms_file():
    text_out = parse_byparms_df()

    save_path = 'byparms_as_text.txt'

    with open(save_path, 'w') as f:
        f.write(text_out)

    custom_tools.openfile(save_path)

    return text_out


def byparms_into_df(test=False):
    if test:
        open_file = r'test.byparms'
    else:
        open_file = custom_tools.getfile('select the byonic parameter file', '.byparms')

    return pd.read_table(open_file, skiprows=range(9), delimiter='=')


def parse_byparms_df():
    # initialise the desired dictionary keys
    salient_dict_keys = initialise_salient_dict_keys()

    # get the byparms as df
    df_byparms = byparms_into_df(test=False)

    # slice out the desired parameters as a dictionary
    salient_dict = get_salient_info_as_dict(df_byparms, salient_dict_keys)

    # parse certain values of the dict
    salient_dict = parse_and_update_certain_dict_values(salient_dict)

    # convert to writeup text
    text_parameters = write_byparms_as_method_text(salient_dict)

    return text_parameters


def parse_multiline_string(s):
    """
    this converts a multiline string into a list of individual lines=entries, stripped of white spaces
    and \n newlines.
    :param s:
    :return:
    """
    result = [x.strip() for x in s.strip().split('\n')]
    return result


def initialise_salient_dict_keys():
    """
    df_index : human readable string
    :return:
    """
    desired_dict_keys_as_multiline_string = \
    """
    PARAMETER_VERSION    
    SpectraFiles
    DatabaseFiles
    add_decoys
    OutputFolder
    machine_type
    precursor_mass_error
    fragment_mass_error
    fragment_mass_error2
    lock_mass_list
    off_by_one
    protein_fdr_pulldown
    DigestLetters
    DigestCutterType
    DigestType
    maximum_missed_cleavages
    glycan_text
    common_max
    rare_max
    mod_text
    enable_promote_score_nglycan
    fragment_unit
    fragment_unit2
    """
    return parse_multiline_string(desired_dict_keys_as_multiline_string)


def get_salient_info_as_dict(df_byparms, salient_dict_keys):
    # extract desired rows
    salient_df = df_byparms.loc[salient_dict_keys,:]
    # convert to a series
    salient_df = salient_df.T.iloc[0,:].fillna(value='not set')
    return salient_df.to_dict()


def parse_and_update_certain_dict_values(salient_dict):

    salient_dict['DigestType'] = parse_digest_type(salient_dict['DigestType'])
    salient_dict['machine_type'] = parse_machine_type_into_fragmentation(salient_dict['machine_type'])
    salient_dict['DigestCutterType'] = parse_digestcuttertype(salient_dict['DigestCutterType'])
    salient_dict['off_by_one'] = parse_off_by_one(salient_dict['off_by_one'])
    salient_dict['add_decoys'] = parse_add_decoys(salient_dict['add_decoys'])
    salient_dict['mod_text'] = parse_mod_text(salient_dict['mod_text'])
    salient_dict['glycan_text'] = parse_mod_text(salient_dict['glycan_text'])
    salient_dict['protein_fdr_pulldown'] = parse_protein_fdr(salient_dict['protein_fdr_pulldown'])
    salient_dict['fragment_unit'] = parse_fragment_unit(salient_dict['fragment_unit'])
    salient_dict['fragment_unit2'] = parse_fragment_unit(salient_dict['fragment_unit2'])

    return salient_dict


def write_byparms_as_method_text(salient_dict):

    results = {}

    results['inputs_and_outputs'] = 'The spectra file was {SpectraFiles}.\nThe FASTA file was {DatabaseFiles}, with decoys {add_decoys}added.\nThe output folder was {OutputFolder}.'.format(**salient_dict)
    results['digestion'] = 'The cleavage sites were set to {DigestType}, {DigestCutterType} of {DigestLetters} with {maximum_missed_cleavages} missed cleavages.'.format(**salient_dict)
    results['instrument'] = 'The database search had the following parameters: precursor m/z tolerance of {precursor_mass_error} ppm; fragmentation type set to {machine_type}, HCD fragment m/z tolerance of {fragment_mass_error} {fragment_unit} and ETD/EThcD fragment m/z tolerance of {fragment_mass_error2} {fragment_unit2}; lock mass was {lock_mass_list}.'.format(**salient_dict)
    results[
        'modifications'] = 'Allowed modification was set at {mod_text}, with maximum of {common_max} common and {rare_max} rare modifications.'.format(**salient_dict)
    results[
        'glycans'] = 'The glycosylation file(s) were {glycan_text}].'.format(
        **salient_dict)
    results[
        'advanced'] = 'Precursor off-by-x was set to {off_by_one}. FDR was {protein_fdr_pulldown}.'.format(
        **salient_dict)


    return '\n\n'.join([results[k] for k in results.keys()])


def parse_digest_type(digest_type_int):

    if not isinstance(digest_type_int, int):
        try:
            digest_type_int = int(digest_type_int)
            print('DigestType was forced to integer, resulting in the value of {}'.format(digest_type_int))
        except:
            return 'DigestType could not be converted to integer, having the invalid value of {}'.format(digest_type_int)

    digest_answer_dict = {0:'Non specific (slowest)',
                          1:'Semi specific (slow)',
                          2:'Fully specific (fastest)',
                          3:'Semi specific N-ragged (slow)',
                          4:'Semi specific C-ragged (slow)'}

    return digest_answer_dict[digest_type_int]


def parse_machine_type_into_fragmentation(machine_type_int):
    if not isinstance(machine_type_int, int):
        try:
            machine_type_int = int(machine_type_int)
            print('machine_type was forced to integer, resulting in the value of {}'.format(machine_type_int))
        except:
            return 'machine_type could not be converted to integer, having the invalid value of {}'.format(machine_type_int)

    answer_dict = {0:'CID low energy',
                   1:'TOF-TOF',
                   2:'QTOF / HCD',
                   3:'ETD / ECD',
                   4:'EThcD',
                   5:'NETD',
                   6:'UVPD',
                   7:'NUVPD',
                   8:'Both: HCD & ETD',
                   9:'Both: CID & ETD',
                   10:'Both: CID & HCD',
                   11:'Both HCD & EThcD',
                   }

    return answer_dict[machine_type_int]


def parse_digestcuttertype(digest_cutter_type_int):
    if not isinstance(digest_cutter_type_int, int):
        try:
            digest_cutter_type_int = int(digest_cutter_type_int)
            print('DigestCutterType was forced to integer, resulting in the value of {}'.format(digest_cutter_type_int))
        except:
            return 'DigestCutterType could not be converted to integer, having the invalid value of {}'.format(digest_cutter_type_int)

    answer_dict = {0:'C-terminal',
                   1:'N-terminal',
                   2:'C-terminal; N-terminal',
                   }

    return answer_dict[digest_cutter_type_int]


def parse_off_by_one(off_by_one_int):
    if not isinstance(off_by_one_int, int):
        try:
            off_by_one_int = int(off_by_one_int)
            print('off_by_one was forced to integer, resulting in the value of {}'.format(off_by_one_int))
        except:
            return 'off_by_one could not be converted to integer, having the invalid value of {}'.format(off_by_one_int)

    answer_dict = {0:'No error check',
                   1:'Too high (narrow)',
                   2:'Too high (wide)',
                   3:'Too high or low (narrow)',
                   4: 'Too high or low (wide)',
                   }

    return answer_dict[off_by_one_int]

def parse_add_decoys(add_decoys_int):
    if not isinstance(add_decoys_int, int):
        try:
            add_decoys_int = int(add_decoys_int)
            print('add_decoys_int was forced to integer, resulting in the value of {}'.format(add_decoys_int))
        except:
            return 'add_decoys_int could not be converted to integer, having the invalid value of {}'.format(add_decoys_int)

    answer_dict = {0:'not ',
                   1:'',
                   }

    return answer_dict[add_decoys_int]

def parse_mod_text(mod_text):
    # remove the tailpiece of % custom text etc, and any line breaks.
    return re.sub('\\\\n%.*','', str(mod_text)).replace('\\n',', ').replace(r'file\:///','')

def parse_protein_fdr(fdr_int):
    if not isinstance(fdr_int, int):
        try:
            fdr_int = int(fdr_int)
            print('off_by_one was forced to integer, resulting in the value of {}'.format(fdr_int))
        except:
            return 'off_by_one could not be converted to integer, having the invalid value of {}'.format(fdr_int)

    answer_dict = {0:'1%',
                   1:'2%',
                   2:'not applied'
                   }

    return answer_dict[fdr_int]

def parse_fragment_unit(fragment_unit_int):
    if not isinstance(fragment_unit_int, int):
        try:
            fragment_unit_int = int(fragment_unit_int)
            print('off_by_one was forced to integer, resulting in the value of {}'.format(fragment_unit_int))
        except:
            return 'off_by_one could not be converted to integer, having the invalid value of {}'.format(fragment_unit_int)

    answer_dict = {0:'ppm',
                   1:'Da',
                   }

    return answer_dict[fragment_unit_int]



if __name__ == '__main__':
    # df = byparms_into_df()
    # byparms = get_text_from_byparms_file()
    # print(byparms)
    g = gui()