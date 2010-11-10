#!/usr/bin/env python
""" Generate python module (qrcode.mem) from QR Code data files.
Just run it in directory which contains 'qrcode' (QR Code python library)
and 'qrcode_data' subdirs.
"""
import hubarcode.qrcode.isodata as isodata
import cPickle
import os


ROOT_DIR = os.path.dirname(__file__)
QRCODE_DIR = os.path.join(ROOT_DIR, 'qrcode')
QRCODE_DATA_DIR = os.path.join(QRCODE_DIR, 'qrcode_data')


matrix_d_dict = {}
format_info_dict = {}
rs_ecc_codewords_dict = {}
rs_block_order_dict = {}
rs_cal_table_dict = {}
frame_data_dict = {}


for version in range(1, 41):
    for ecl in range(0, 4):
        byte_num = (isodata.MATRIX_REMAIN_BIT[version] +
                        (isodata.MAX_CODEWORDS[version] << 3))

        filename = 'qrv%s_%s.dat' % (version, ecl)
        filename = os.path.join(QRCODE_DATA_DIR, filename)
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

        key = '%s_%s' % (version, ecl)
        matrix_d_dict[key] = matrix_d
        format_info_dict[key] = format_info
        rs_ecc_codewords_dict[key] = rs_ecc_codewords
        rs_block_order_dict[key] = rs_block_order

        filename = 'rsc%s.dat' % rs_ecc_codewords
        filename = os.path.join(QRCODE_DATA_DIR, filename)
        fhndl = open(filename, "rb")

        rs_cal_table = []
        for _ in range(0, 256):
            rs_cal_table.append(unpack(fhndl.read(rs_ecc_codewords)))
        # end for
        fhndl.close()

        rs_cal_table_dict[rs_ecc_codewords] = rs_cal_table

    filename = 'qrvfr%s.dat' % version
    filename = os.path.join(QRCODE_DATA_DIR, filename)
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

    frame_data_dict[version] = frame_data


mem = open('qrcode/mem.py', 'w')
mem.write('matrix_d = %s\n' % repr(matrix_d_dict))
mem.write('format_info = %s\n' % repr(format_info_dict))
mem.write('rs_ecc_codewords = %s\n' % repr(rs_ecc_codewords_dict))
mem.write('rs_block_order = %s\n' %  repr(rs_block_order_dict))
mem.write('rs_cal_table = %s\n' % repr(rs_cal_table_dict))
mem.write('frame_data = %s\n' % repr(frame_data_dict))
mem.close()