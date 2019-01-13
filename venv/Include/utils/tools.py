import json
import collections


def get_proxy_dict(port):
    return {
            "http": "http://" + port,
            "https": "https://" + port,
            "ftp": "ftp://10.10.1.10:3128"
        }


def load_json_file(filename, use_ordered_dict=True):
    """ Load a dictionary from a file

    Parameters
    ----------
    * filename: string
    \tThe path to the saved json file.
    * use_ordered_dict: bool
    \tIf set to True dicts are read as OrderedDicts.
    """
    tmp = None
    with open(filename, 'r') as infile:
        if use_ordered_dict:
            tmp = json.JSONDecoder(
                object_pairs_hook=collections.OrderedDict).decode(
                infile.read())
        else:
            tmp = json.load(infile)
        infile.close()
    return tmp