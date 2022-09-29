
# seperate script

import os
import pandas as pd


    
    
from collections import defaultdict

def load_ko_from_dram(dram_annotation_file,get_names=False):

    genome_ko=defaultdict(int)
    ko_names= {}

    with open(dram_annotation_file) as f:
        #read header line
        f.readline()
        
        for line in f:
            elements= line.split('\t')

            KO_list = elements[8]

            if KO_list!='':

                genome= elements[1]

                if get_names:
                    
                    for ko,description in zip(KO_list.split(','), elements[9].split('; ')):
                        genome_ko[(genome,ko)]+= 1
                
                    if not ko in ko_names:
                        ko_names[ko]=description
                else:
                    
                    for ko in KO_list.split(','):
                        genome_ko[(genome,ko)]+= 1
                    
                
                    
    if get_names:
        return pd.Series(genome_ko), pd.Series(ko_names,name='KO name')
    else:
        return pd.Series(genome_ko)

def load_modules(dram_folder,threshold= 0.75, plot=False):


    dram_file = os.path.join(dram_folder,"annotations.tsv")
    module_file= os.path.join(dram_folder,"kegg_modules.tsv") #

    module_table= pd.read_table(module_file, index_col=[1,2])
    module_matrix= module_table.step_coverage.unstack(fill_value=0)
    module_matrix= module_matrix.loc[:, module_matrix.max()>0.1]


    module_names = module_table.droplevel(0).module_name.drop_duplicates()

    
    #drop all 0 modules
    #module_presence= module_presence.loc[:,module_presence.max()>0]


    # calculate module coverage
    module_presence = (module_matrix > threshold) *1

    
    if plot:
        import seaborn as sns
        cgi= sns.clustermap(module_matrix,metric='cosine',figsize=(12,10),row_cluster=False)

        cgi_bin=sns.clustermap(module_matrix> threshold,
                    figsize=(12,10),
                    row_cluster=False,
                        col_linkage= cgi.dendrogram_col.linkage
                    )


    # add SCFA miself
    
    ko=load_ko_from_dram(dram_file).unstack(fill_value=0)





    paths_for= {'Propanoate' : [('K19697','K00932'),'K01026','K01895','K01908'],
                    'Butyrate': [('K01034','K01034'),('K00929','K00634')] ,
                'Acetate': ['K01067','K00156','K00925','K01512','K00467'
                            #('K00467','K00016'),
                            #('K01895','K01913','K01895','K01913'),
                            #('K01026','K18118'),('K01026','K01905','K22224','K24012')
                        ],
                'Lactate': ['K00016']
                    
                        
                        }

    F = pd.DataFrame(index=ko.index)

    for function in paths_for:

        F[function]= False

        for ko_list in  paths_for[function]:

            if type(ko_list)==str:
                ko_list = [ko_list]

                
            F[function] |= ko.reindex(columns=ko_list,fill_value=False).all(1)
            
            #print(f"{function} {ko_list} {ko.reindex(columns=ko_list,fill_value=False).all(1).sum() / ko.shape[0]}")


    module_presence= pd.concat( (module_presence,F.astype(int)),axis=1)

    for scfa in F.columns:
        module_names[scfa]= scfa



    return module_presence, module_names, ko
