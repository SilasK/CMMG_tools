
from importlib.resources import path
import pandas as pd
import numpy as np

import pathlib2 as pathlib
from regex import F
from .taxonomy import tax2table

from .shell import wget

CMMG_URL= "https://ezmeta.unige.ch/CMMG"

TAXONOMY_FILE= "Supplementary_Tables_and_Figures/Tables/Table_S4_curated_taxonomy.tsv"


DATA_PATH = pathlib.Path(__file__).parent.parent.absolute()/"data"



def use_local_copy_of_file(file_path):

    local_file = DATA_PATH/file_path

    if not local_file.exists():

        print(f"Downloading {file_path} from CMMG and store local copy")

        output_dir= str((DATA_PATH / file_path ).parent)

        wget( f"{CMMG_URL}/{file_path}", output_dir=  output_dir
        )

    return local_file






def load_taxonomy(host, remove_prefix=True):
    """
    Loads the curated taxonomy. If local file exists, it is used, otherwise it downloads from the server

    Parameters
    -----------
    host: str   microbiome host ['human','mouse','both']
    """

    tax_file= use_local_copy_of_file(TAXONOMY_FILE)

    gg_tax= pd.read_table(tax_file,header=None, index_col=0)

    Tax = tax2table(gg_tax.squeeze(), remove_prefix=remove_prefix)


    if host=='human':
        Tax= Tax[Tax.index.str[:3]=="GUT"]
    elif host=='mouse':
        Tax= Tax[Tax.index.str[:3]=="MGG"]
    elif host=='both':
        pass
    else:
        raise ValueError(f"host must be one of ['human','mouse','both'] but is {host}")

    return Tax

    
        