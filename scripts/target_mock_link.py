import numpy as np
import os
import argparse
import yaml

from desitarget.mock.io import decode_rownum_filenum
from astropy.table import Table


parser = argparse.ArgumentParser()
parser.add_argument('--config','-c',default='input.yaml')
parser.add_argument("--input_dir", "-I", help="Path to the truth.fits and target.fits files", type=str, default="./")
args = parser.parse_args()


with open(args.config,'r') as pfile:
    params = yaml.load(pfile)


#defines the target and variable to recover from the mock
source_name = 'MWS_MAIN'
variable_to_recover = 'vX'

# load the map_id_filename
map_id_filename = np.loadtxt(os.path.join(args.input_dir,'map_id_filename.txt'), 
                             dtype={'names': ('SOURCENAME', 'FILEID', 'FILENAME'),
                                   'formats': ('S10', 'i4', 'S256')})
# load truth
truth_table = Table.read(os.path.join(args.input_dir, 'truth.fits'))
print('loaded {} truth items'.format(len(truth_table)))

# load targets
target_table = Table.read(os.path.join(args.input_dir, 'targets.fits'))
print('loaded {} target items'.format(len(target_table)))

# decode rowid and fileid for the targets of interest
ii = truth_table['SOURCETYPE']==source_name
rowid, fileid = decode_rownum_filenum(truth_table['MOCKID'][ii])

# get the fileids to be read
fileid_to_read = np.array(list(set(fileid)))
print('fileid to be read {}'.format(fileid_to_read))

# prepare the arrays to save the variable to match
n = np.count_nonzero(ii)
to_recover = np.empty((0))


for i in fileid_to_read:
    ii = (map_id_filename['SOURCENAME']==source_name.encode()) & (map_id_filename['FILEID']==i)

    filename = map_id_filename['FILENAME'][ii]
    filename = filename[0].decode()
    print('reading {}'.format(filename))
    result = Table.read(filename)

    rows_to_get = rowid[fileid==i]
    to_recover = np.append(to_recover, result[variable_to_recover][rows_to_get])






