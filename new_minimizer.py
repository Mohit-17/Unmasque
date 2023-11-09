import copy

import pandas as pd

from .abstract.MinimizerBase import Minimizer
from ..refactored.util.common_queries import get_row_count, alter_table_rename_to, get_min_max_ctid, \
    drop_view, drop_table, create_table_as_select_star_from, get_ctid_from, get_tabname_1, \
    create_view_as_select_star_where_ctid, create_table_as_select_star_from_ctid, get_tabname_4, get_star, \
    get_restore_name,get_freq,delete_non_matching_rows,create_table_like
from ..refactored.util.utils import isQ_result_empty

class NewMinimizer(Minimizer):


    def __init__(self, connectionHelper,
                 core_relations, core_sizes,global_all_attribs):
        super().__init__(connectionHelper, core_relations, core_sizes,global_all_attribs, "New_Minimizer")
        # self.cs2_passed = sampling_status

        self.global_other_info_dict = {}
        self.global_result_dict = {}
        self.local_other_info_dict = {}
        self.global_min_instance_dict = {}
       # self.global_all_attribs =[]

    def extract_params_from_args(self, args):
        return args[0]
    
    def doActualJob(self, args):
        query = self.extract_params_from_args(args)
        return self.frequency_counter( query)
    
    
    def frequency_counter(self, query):
        for i in range(len(self.core_relations)):
            tabname = self.core_relations[i]
            attrib_list = self.global_all_attribs[i]

            for attrib in attrib_list:
                #row_count = get_row_count(tabname)
                #freq_dict = {};

                freq_count = pd.read_sql_query(get_freq(tabname,attrib),self.connectionHelper.conn)  
                df = pd.DataFrame(freq_count)
                print(df)
                for i in range(len(df.index)):
                    # max_freq_count = df.iloc[i]['counter']
                    max_freq_val = df.iloc[i]['attrib']
                    print("max val"+max_freq_val)
                    try:
                        self.connectionHelper.execute_sql(
                            ["BEGIN;", alter_table_rename_to(tabname,"tabname1") , 
                              create_table_as_select_star_from(get_tabname_1(tabname), tabname),
                                delete_non_matching_rows(tabname,attrib,max_freq_val)])
                        #print(1)
                        size = self.connectionHelper.execute_sql_fetchone_0(get_row_count(tabname))
                        print("Size"+size)
                        result = self.app.doJob(query)
                        if isQ_result_empty(result) == False:
                            break

                    except Exception as error:
                        print("Error Occurred in  minimizer. Error: " + str(error))
                        self.connectionHelper.execute_sql(["ROLLBACK;"])
                        exit(1)

                    # self.connectionHelper.execute_sql(["ROLLBACK;"])
                    

                    



                
                    

            
    

    