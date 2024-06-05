# -*- coding: utf-8 -*-
"""
Created on Sat May  4 00:56:11 2024

@author: ronbinyamin
"""
def update_line(line,load_count):
    if 'Residential' in line or 'Commercial_SM' in line or 'Commercial_MD' in line:
        line = line.replace('Residential', f'LS{load_count}')
        line = line.replace('Commercial_SM', f'LS{load_count}')
        line = line.replace('Commercial_MD', f'LS{load_count}')
    elif 'yearly' in line:
        index_yearly = line.find('yearly')
        if index_yearly != -1:
            # Replace from 'yearly' onwards with the new load shape definition
            line = line[:index_yearly] + f'yearly=LS{load_count}\n'
    elif 'yearly' not in line:
        # Append 'yearly=' with the current load shape number to lines not already covered
        line = line.rstrip() + ' yearly=LS' + str(load_count) + '\n'
    return line
def update_loadshape(numOfLoads,LOADS_FILE,OUTPUT_FILE,npts1):
    # this part create loadshape.dss files
    with open(OUTPUT_FILE, 'w') as f:
        for i in range(1, numOfLoads + 1, 1):
            f.write('New LoadShape.LS' + str(i) +' ' + 'npts=' + str(npts1) + ' ' + 'interval=1.0 Pmult=(File=LS' + str(i) + '.csv) Qmult=(File=LS_Q' + str(i) + '.csv)' + '\n')

    # this part edit the loadshape corresponding to each load
    # orginially ckt5 has only 3 type of loadsahpes (that is each one of the hunderds of loads in it has one of three loadshapes)
    # this code makes dure that each load has a unique loadshape
    with open(LOADS_FILE,'r') as f_in:
        raw_file_lines = f_in.readlines()
    with open(LOADS_FILE,'w') as f_out: 
        load_count = 1
        #with open(OUTPUT_FILE, 'w') as f_out:
        for line in raw_file_lines:
            if 'New Load' in line:
                comment_pos = line.find('!')
                # Insert 'yearly=LS{load_count}' before comment if exists, otherwise at the end
                if comment_pos != -1:
                    part1 = update_line(line[:comment_pos],load_count) # Text before the comment
                    part2 = line[comment_pos:]  # The comment itself
                    line = f'{part1}{part2}'
                    load_count += 1
                else:                        
                    line = update_line(line,load_count)
                    load_count += 1
            f_out.write(line)
                    

#update_loadshape(91,r"C:\Program Files\OpenDSS\IEEETestCases\123Bus\IEEE123Loads.DSS",r"C:\Program Files\OpenDSS\IEEETestCases\123Bus\IEEE123Loads123.DSS")