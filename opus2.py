#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: O 2
# Author: ardiu
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import fec
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import iio
import opus2_epy_block_0_0 as epy_block_0_0  # embedded python block
import opus2_epy_block_2_0 as epy_block_2_0  # embedded python block
import sip
import threading



class opus2(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "O 2", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("O 2")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "opus2")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.qpsk = qpsk = digital.constellation_rect([-0.707-0.707j, 0.707-0.707j, +0.707+0.707j, -0.707+0.707j], [0, 1, 3, 2],
        4, 2, 2, 1, 1).base()
        self.sps = sps = 4
        self.samp_rate_2 = samp_rate_2 = 48000
        self.samp_rate = samp_rate = 300000
        self.phase_bw = phase_bw = 0.0628
        self.hdr = hdr = digital.header_format_default(digital.packet_utils.default_access_code, 0)
        self.excess_bw = excess_bw = 0.35
        self.decoder = decoder = fec.cc_decoder.make(1280,7, 2, [79,109], 0, (-1), fec.CC_TRUNCATED, False)
        self.cma_algo = cma_algo = digital.adaptive_algorithm_cma( qpsk, .0001, 1).base()

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_eye_sink_x_0_1 = qtgui.eye_sink_c(
            1024, #size
            samp_rate, #samp_rate
            1, #number of inputs
            None
        )
        self.qtgui_eye_sink_x_0_1.set_update_time(0.10)
        self.qtgui_eye_sink_x_0_1.set_samp_per_symbol(sps)
        self.qtgui_eye_sink_x_0_1.set_y_axis(-1, 1)

        self.qtgui_eye_sink_x_0_1.set_y_label('Amplitude', "")

        self.qtgui_eye_sink_x_0_1.enable_tags(True)
        self.qtgui_eye_sink_x_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_eye_sink_x_0_1.enable_autoscale(False)
        self.qtgui_eye_sink_x_0_1.enable_grid(False)
        self.qtgui_eye_sink_x_0_1.enable_axis_labels(True)
        self.qtgui_eye_sink_x_0_1.enable_control_panel(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'blue', 'blue', 'blue', 'blue',
            'blue', 'blue', 'blue', 'blue', 'blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [3, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_eye_sink_x_0_1.set_line_label(i, "Eye [Re{{Data {0}}}]".format(round(i/2)))
                else:
                    self.qtgui_eye_sink_x_0_1.set_line_label(i, "Eye [Im{{Data {0}}}]".format(round((i-1)/2)))
            else:
                self.qtgui_eye_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_eye_sink_x_0_1.set_line_width(i, widths[i])
            self.qtgui_eye_sink_x_0_1.set_line_color(i, colors[i])
            self.qtgui_eye_sink_x_0_1.set_line_style(i, styles[i])
            self.qtgui_eye_sink_x_0_1.set_line_marker(i, markers[i])
            self.qtgui_eye_sink_x_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_eye_sink_x_0_1_win = sip.wrapinstance(self.qtgui_eye_sink_x_0_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_eye_sink_x_0_1_win)
        self.qtgui_const_sink_x_0_1 = qtgui.const_sink_c(
            1024, #size
            'Synced Constellation', #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_1.set_update_time(0.10)
        self.qtgui_const_sink_x_0_1.set_y_axis((-1.5), 1.5)
        self.qtgui_const_sink_x_0_1.set_x_axis((-1.5), 1.5)
        self.qtgui_const_sink_x_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_1.enable_autoscale(False)
        self.qtgui_const_sink_x_0_1.enable_grid(True)
        self.qtgui_const_sink_x_0_1.enable_axis_labels(True)


        labels = ['Synced Only', 'Synced & Phase-Locked', '', '', '',
            '', '', '', '', '']
        widths = [1, 2, 2, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 1, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, -1, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1, 0.3, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_1.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_1.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_1.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_1.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_1_win = sip.wrapinstance(self.qtgui_const_sink_x_0_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_1_win, 2, 0, 10, 10)
        for r in range(2, 12):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 10):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.iio_pluto_source_0_0 = iio.fmcomms2_source_fc32('usb:' if 'usb:' else iio.get_pluto_uri(), [True, True], 16384)
        self.iio_pluto_source_0_0.set_len_tag_key('packet_len')
        self.iio_pluto_source_0_0.set_frequency(868300000)
        self.iio_pluto_source_0_0.set_samplerate(samp_rate)
        self.iio_pluto_source_0_0.set_gain_mode(0, 'slow_attack')
        self.iio_pluto_source_0_0.set_gain(0, 64)
        self.iio_pluto_source_0_0.set_quadrature(True)
        self.iio_pluto_source_0_0.set_rfdc(True)
        self.iio_pluto_source_0_0.set_bbdc(True)
        self.iio_pluto_source_0_0.set_filter_params('Auto', '', 0, 0)
        self.filter_fft_rrc_filter_0_0_1 = filter.fft_filter_ccc(1, firdes.root_raised_cosine(1, samp_rate, (samp_rate/sps), excess_bw, (sps*25)), 1)
        self.fec_extended_decoder_0_0 = fec.extended_decoder(decoder_obj_list=decoder, threading= None, ann=None, puncpat='11', integration_period=10000)
        self.epy_block_2_0 = epy_block_2_0.rsa_decrypt_byte(private_d=153, n=253)
        self.epy_block_0_0 = epy_block_0_0.opus_decoder_stream(sample_rate=48000)
        self.digital_symbol_sync_xx_0_1 = digital.symbol_sync_cc(
            digital.TED_MUELLER_AND_MULLER,
            sps,
            0.01,
            1,
            2.7,
            1.5,
            1,
            digital.constellation_qpsk().base(),
            digital.IR_MMSE_8TAP,
            128,
            [])
        self.digital_map_bb_0_0_1 = digital.map_bb([0,1,3,2])
        self.digital_map_bb_0_0 = digital.map_bb([-1,1])
        self.digital_linear_equalizer_0 = digital.linear_equalizer(2, 1, cma_algo, True, [ ], 'corr_est')
        self.digital_fll_band_edge_cc_0_0 = digital.fll_band_edge_cc(sps, 0.350, 55, 0.005)
        self.digital_diff_decoder_bb_0_1 = digital.diff_decoder_bb(4, digital.DIFF_DIFFERENTIAL)
        self.digital_crc32_bb_1 = digital.crc32_bb(True, 'packet_len', True)
        self.digital_costas_loop_cc_0_1 = digital.costas_loop_cc(phase_bw, 4, False)
        self.digital_correlate_access_code_xx_ts_0_0 = digital.correlate_access_code_bb_ts(digital.packet_utils.default_access_code,
          2, 'packet_len')
        self.digital_constellation_decoder_cb_0_1 = digital.constellation_decoder_cb(qpsk)
        self.digital_additive_scrambler_xx_1 = digital.additive_scrambler_bb(0x8A, 0x7F, 8, count=0, bits_per_byte=3, reset_tag_key="")
        self.blocks_unpack_k_bits_bb_1_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_unpack_k_bits_bb_0_2 = blocks.unpack_k_bits_bb(2)
        self.blocks_repack_bits_bb_1 = blocks.repack_bits_bb(1, 8, 'packet_len', True, gr.GR_MSB_FIRST)
        self.blocks_pack_k_bits_bb_0_0 = blocks.pack_k_bits_bb(8)
        self.blocks_matrix_interleaver_0_0 = blocks.matrix_interleaver(
            itemsize=gr.sizeof_char * 1, rows=32, cols=80, deint=True
        )
        self.blocks_char_to_float_0_0 = blocks.char_to_float(1, 1)
        self.audio_sink_0_0_0 = audio.sink(48000, '', True)
        self.analog_agc_xx_0_0 = analog.agc_cc((0.005e-3), 1, 1, 20)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc_xx_0_0, 0), (self.digital_fll_band_edge_cc_0_0, 0))
        self.connect((self.blocks_char_to_float_0_0, 0), (self.fec_extended_decoder_0_0, 0))
        self.connect((self.blocks_matrix_interleaver_0_0, 0), (self.digital_map_bb_0_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0_0, 0), (self.digital_additive_scrambler_xx_1, 0))
        self.connect((self.blocks_repack_bits_bb_1, 0), (self.digital_crc32_bb_1, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0_2, 0), (self.digital_correlate_access_code_xx_ts_0_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_1_0, 0), (self.blocks_matrix_interleaver_0_0, 0))
        self.connect((self.digital_additive_scrambler_xx_1, 0), (self.epy_block_2_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_1, 0), (self.digital_diff_decoder_bb_0_1, 0))
        self.connect((self.digital_correlate_access_code_xx_ts_0_0, 0), (self.blocks_repack_bits_bb_1, 0))
        self.connect((self.digital_costas_loop_cc_0_1, 0), (self.digital_constellation_decoder_cb_0_1, 0))
        self.connect((self.digital_costas_loop_cc_0_1, 0), (self.qtgui_const_sink_x_0_1, 1))
        self.connect((self.digital_costas_loop_cc_0_1, 0), (self.qtgui_eye_sink_x_0_1, 0))
        self.connect((self.digital_crc32_bb_1, 0), (self.blocks_unpack_k_bits_bb_1_0, 0))
        self.connect((self.digital_diff_decoder_bb_0_1, 0), (self.digital_map_bb_0_0_1, 0))
        self.connect((self.digital_fll_band_edge_cc_0_0, 0), (self.digital_symbol_sync_xx_0_1, 0))
        self.connect((self.digital_linear_equalizer_0, 0), (self.digital_costas_loop_cc_0_1, 0))
        self.connect((self.digital_map_bb_0_0, 0), (self.blocks_char_to_float_0_0, 0))
        self.connect((self.digital_map_bb_0_0_1, 0), (self.blocks_unpack_k_bits_bb_0_2, 0))
        self.connect((self.digital_symbol_sync_xx_0_1, 0), (self.digital_linear_equalizer_0, 0))
        self.connect((self.digital_symbol_sync_xx_0_1, 0), (self.qtgui_const_sink_x_0_1, 0))
        self.connect((self.epy_block_0_0, 0), (self.audio_sink_0_0_0, 0))
        self.connect((self.epy_block_2_0, 0), (self.epy_block_0_0, 0))
        self.connect((self.fec_extended_decoder_0_0, 0), (self.blocks_pack_k_bits_bb_0_0, 0))
        self.connect((self.filter_fft_rrc_filter_0_0_1, 0), (self.analog_agc_xx_0_0, 0))
        self.connect((self.iio_pluto_source_0_0, 0), (self.filter_fft_rrc_filter_0_0_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "opus2")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_qpsk(self):
        return self.qpsk

    def set_qpsk(self, qpsk):
        self.qpsk = qpsk
        self.digital_constellation_decoder_cb_0_1.set_constellation(self.qpsk)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.digital_symbol_sync_xx_0_1.set_sps(self.sps)
        self.filter_fft_rrc_filter_0_0_1.set_taps(firdes.root_raised_cosine(1, self.samp_rate, (self.samp_rate/self.sps), self.excess_bw, (self.sps*25)))
        self.qtgui_eye_sink_x_0_1.set_samp_per_symbol(self.sps)

    def get_samp_rate_2(self):
        return self.samp_rate_2

    def set_samp_rate_2(self, samp_rate_2):
        self.samp_rate_2 = samp_rate_2

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.filter_fft_rrc_filter_0_0_1.set_taps(firdes.root_raised_cosine(1, self.samp_rate, (self.samp_rate/self.sps), self.excess_bw, (self.sps*25)))
        self.iio_pluto_source_0_0.set_samplerate(self.samp_rate)
        self.qtgui_eye_sink_x_0_1.set_samp_rate(self.samp_rate)

    def get_phase_bw(self):
        return self.phase_bw

    def set_phase_bw(self, phase_bw):
        self.phase_bw = phase_bw
        self.digital_costas_loop_cc_0_1.set_loop_bandwidth(self.phase_bw)

    def get_hdr(self):
        return self.hdr

    def set_hdr(self, hdr):
        self.hdr = hdr

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw
        self.filter_fft_rrc_filter_0_0_1.set_taps(firdes.root_raised_cosine(1, self.samp_rate, (self.samp_rate/self.sps), self.excess_bw, (self.sps*25)))

    def get_decoder(self):
        return self.decoder

    def set_decoder(self, decoder):
        self.decoder = decoder

    def get_cma_algo(self):
        return self.cma_algo

    def set_cma_algo(self, cma_algo):
        self.cma_algo = cma_algo




def main(top_block_cls=opus2, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
