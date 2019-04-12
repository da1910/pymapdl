"""
ANSYS-written binary files include the following:

The following results files, in which the ANSYS program stores the
results of solving finite element analysis problems:
- Jobname.RST A structural or coupled-field analysis
- Jobname.RTH A thermal analysis
- Jobname.RMG A magnetic analysis
- Jobname.RFL A FLOTRAN analysis (a legacy results file)
- The Jobname.MODE file, storing data related to a modal analysis
- The Jobname.RDSP file, storing data related to a mode-superposition transient analysis.
- Jobname.RFRQ file, storing data related to a mode-superposition harmonic analysis
- Jobname.EMAT file, storing data related to element matrices
- Jobname.SUB file, storing data related to substructure matrices
- Jobname.FULL file, storing the full stiffness-mass matrix
- Jobname.DSUB file, storing displacements related to substructure matrices

Documentation taken from:
https://www.sharcnet.ca/Software/Ansys/16.2.3/en-us/help/ans_prog/Hlp_P_INT1_1.html
Thanks!

"""
import os
import numpy as np

from pyansys.common import read_string_from_binary, read_table
import pyansys

# FILE_FORMAT = {2: 

def read_binary(filename):
    return BinaryFile(filename)


class BinaryFile(object):
    """
    https://stackoverflow.com/questions/12099237
    """

    def __init__(self, filename):
        """Reads standard header"""
        if not os.path.isfile(filename):
            raise FileNotFoundError('%s is not a file or cannot be found' %
                                    str(filename))

        self.filename = filename
        self.standard_header = read_standard_header(self.filename)
        file_format = self.standard_header['file format'] 

        if file_format== 2:
            from pyansys.emat import EmatFile
            self.__class__ = EmatFile
            self.__init__()

        elif file_format== 4:
            from pyansys.full import FullFile
            self.__class__ = FullFile
            self.__init__()

        elif file_format== 12:
            from pyansys.rst import ResultFile
            self.__class__ = ResultFile
            self.__init__()

        else:
            raise RuntimeError('Result type %s is not yet supported' %
                               str(file_format))


def read_standard_header(filename):
    """ Reads standard header """
    with open(filename, 'rb') as f:

        endian = '<'
        if np.fromfile(f, dtype='<i', count=1) != 100:

            # Check if big enos
            f.seek(0)
            if np.fromfile(f, dtype='>i', count=1) == 100:
                endian = '>'

            # Otherwise, it's probably not a result file
            else:
                raise Exception('Unable to determine endian type.  ' +
                                'Possibly not an ANSYS binary file')

        f.seek(0)

        header = {}
        header['endian'] = endian
        header['file number'] = read_table(f, nread=1, get_nread=False)[0]
        header['file format'] = read_table(f, nread=1, get_nread=False)[0]
        int_time = str(read_table(f, nread=1, get_nread=False)[0])
        header['time'] = ':'.join([int_time[0:2], int_time[2:4], int_time[4:]])
        int_date = str(read_table(f, nread=1, get_nread=False)[0])
        if int_date == '-1':
            header['date'] = ''
        else:
            header['date'] = '/'.join([int_date[0:4], int_date[4:6], int_date[6:]])

        unit_types = {0: 'User Defined',
                      1: 'SI',
                      2: 'CSG',
                      3: 'U.S. Customary units (feet)',
                      4: 'U.S. Customary units (inches)',
                      5: 'MKS',
                      6: 'MPA',
                      7: 'uMKS'}
        header['units'] = unit_types[read_table(f, nread=1, get_nread=False)[0]]

        f.seek(11 * 4)
        version = read_string_from_binary(f, 1).strip()

        header['verstring'] = version
        header['mainver'] = int(version[:2])
        header['subver'] = int(version[-1])

        # there's something hidden at 12
        f.seek(4, 1)

        # f.seek(13 * 4)
        header['machine'] = read_string_from_binary(f, 3).strip()
        header['jobname'] = read_string_from_binary(f, 2).strip()
        header['product'] = read_string_from_binary(f, 2).strip()
        header['special'] = read_string_from_binary(f, 1).strip()
        header['username'] = read_string_from_binary(f, 3).strip()

        # Items 23-25 The machine identifier in integer form (three four-character strings)
        # this contains license information
        header['machine_identifier'] = read_string_from_binary(f, 3).strip()

        # Item 26 The system record size
        header['system record size'] = read_table(f, nread=1, get_nread=False)[0]

        # Item 27 The maximum file length
        # header['file length'] = read_table(f, nread=1, get_nread=False)[0]

        # Item 28 The maximum record number
        # header['the maximum record number'] = read_table(f, nread=1, get_nread=False)[0]

        # Items 31-38 The Jobname (eight four-character strings)
        f.seek(32*4)
        header['jobname2'] = read_string_from_binary(f, 8).strip()

        # Items 41-60 The main analysis title in integer form (20 four-character strings)
        f.seek(42*4)
        header['title'] = read_string_from_binary(f, 20).strip()

        # Items 61-80 The first subtitle in integer form (20 four-character strings)
        header['subtitle'] = read_string_from_binary(f, 20).strip()

        # Item 95 The split point of the file (0 means the file will not split)
        f.seek(96*4)
        header['split point'] = read_table(f, nread=1, get_nread=False)[0]

        # Items 97-98 LONGINT of the maximum file length (bug here)
        # ints = read_table(f, nread=2, get_nread=False)
        # header['file length'] = two_ints_to_long(ints[0], ints[1])

    return header

