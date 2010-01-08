#!/usr/bin/env python
""" Generate python modules from QR Code data files.
Just run it in directory which contains 'qrcode' (QR Code python library)
and 'qrcode_data' subdirs.
"""
import qrcode.isodata as isodata
import cPickle
import os

if not os.path.exists('qrcode/data'):
    os.mkdir('qrcode/data')

INIT = open('qrcode/data/__init__.py', 'w')
INIT.close()

for version in range(1, 41):
    for ecl in range(0, 4):
        byte_num = (isodata.MATRIX_REMAIN_BIT[version] +
                        (isodata.MAX_CODEWORDS[version] << 3))

        filename = "qrcode_data/qrv" + str(version) + "_"
        filename += str(ecl) + ".dat"
        fhndl = open(filename, "rb")
        unpack = lambda y: [ord(x) for x in y]
        matrix_d = []
        matrix_d.append(unpack(fhndl.read(byte_num)))
        matrix_d.append(unpack(fhndl.read(byte_num)))
        matrix_d.append(unpack(fhndl.read(byte_num)))

        format_info = []
        format_info.append(unpack(fhndl.read(15)))
        format_info.append(unpack(fhndl.read(15)))

        rs_ecc_codewords = ord(fhndl.read(1))
        rs_block_order = unpack(fhndl.read(128))
        fhndl.close()

        qrv = open('qrcode/data/qrv%d_%d.py' % (version, ecl), 'w')
        qrv.write('import cPickle\n\n')
        qrv.write('byte_num = %d\n' % byte_num)
        qrv.write('matrix_d = cPickle.loads("""%s""")\n' %
                                                     cPickle.dumps(matrix_d))
        qrv.write('format_info = cPickle.loads("""%s""")\n' %
                                                  cPickle.dumps(format_info))
        qrv.write('rs_ecc_codewords = %d\n' % rs_ecc_codewords)
        qrv.write('rs_block_order = cPickle.loads("""%s""")\n' %
                                               cPickle.dumps(rs_block_order))
        qrv.write('from qrcode.data.rsc%d import rs_cal_table\n' %
                                                            rs_ecc_codewords)
        qrv.write('from qrcode.data.fr%d import frame_data\n' % version)
        qrv.close()

        filename = "qrcode_data/rsc" + str(rs_ecc_codewords) + ".dat"
        fhndl = open(filename, "rb")

        rs_cal_table = []

        for _ in range(0, 256):
            rs_cal_table.append(unpack(fhndl.read(rs_ecc_codewords)))
        # end for
        fhndl.close()

        rsc = open('qrcode/data/rsc%d.py' % rs_ecc_codewords, 'w')
        rsc.write('import cPickle\n\n')
        rsc.write('rs_cal_table = cPickle.loads("""%s""")\n' %
                                                 cPickle.dumps(rs_cal_table))
        rsc.close()

    filename = "qrcode_data/qrvfr" + str(version) + ".dat"
    fhndl = open(filename, "rb")
    frame_data_str = fhndl.read(65535)
    frame_data = []
    for line in frame_data_str.split("\n"):
        frame_line = []
        for char in line:
            if char == '1':
                frame_line.append(1)
            elif char == '0':
                frame_line.append(0)
            else:
                raise ValueError("Corrupted frame data file")
            # end if
        # end for
        frame_data.append(frame_line)
    # end for
    fhndl.close()
    fr = open('qrcode/data/fr%d.py' % version, 'w')
    fr.write('import cPickle\n\n')
    fr.write('frame_data = cPickle.loads("""%s""")\n' %
                                                   cPickle.dumps(frame_data))
    fr.close()
