#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: TX
# Author: ardiu
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import audio
from gnuradio import blocks
from gnuradio import digital
from gnuradio import fec
from gnuradio import filter
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
import RADIO_TX_epy_block_1_0 as epy_block_1_0  # embedded python block
import RADIO_TX_epy_block_2 as epy_block_2  # embedded python block
import sip
import threading



class RADIO_TX(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "TX", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("TX")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "RADIO_TX")

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
        self.samp_rate = samp_rate = 48000
        self.phase_bw = phase_bw = 0.0628
        self.payload_size = payload_size = 320
        self.hdr = hdr = digital.header_format_default(digital.packet_utils.default_access_code, 0)
        self.excess_bw = excess_bw = 0.35
        self.encoder = encoder = fec.cc_encoder_make(1280,7, 2, [79,109], 0, fec.CC_TRUNCATED, False)
        self.cma_algo = cma_algo = digital.adaptive_algorithm_cma( qpsk, .0001, 1).base()

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_time_sink_x_1_1_0_0_0 = qtgui.time_sink_f(
            1024, #size
            48000, #samp_rate
            "Inputed Voice", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1_1_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_1_1_0_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_1_1_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1_1_0_0_0.enable_tags(False)
        self.qtgui_time_sink_x_1_1_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1_1_0_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_1_1_0_0_0.enable_grid(False)
        self.qtgui_time_sink_x_1_1_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_1_1_0_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_1_1_0_0_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1_1_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1_1_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1_1_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1_1_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1_1_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1_1_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1_1_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_1_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_1_1_0_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_1_0_0_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            2048, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            300000, #bw
            'Before and after filter Spectrum', #name
            2,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), (-10))
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['Transmitted & Propagated', 'Received & Filtered', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 12, 0, 10, 20)
        for r in range(12, 22):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 20):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.iio_pluto_sink_0_0 = iio.fmcomms2_sink_fc32('usb:' if 'usb:' else iio.get_pluto_uri(), [True, True], 16384, False)
        self.iio_pluto_sink_0_0.set_len_tag_key('')
        self.iio_pluto_sink_0_0.set_bandwidth(200000)
        self.iio_pluto_sink_0_0.set_frequency(868300000)
        self.iio_pluto_sink_0_0.set_samplerate(300000)
        self.iio_pluto_sink_0_0.set_attenuation(0, 0)
        self.iio_pluto_sink_0_0.set_filter_params('Auto', '', 0, 0)
        self.filter_fft_rrc_filter_0_1 = filter.fft_filter_ccc(1, firdes.root_raised_cosine(1, 300000, (300000/4), excess_bw, (sps*25)), 1)
        self.fec_extended_encoder_0 = fec.extended_encoder(encoder_obj_list=encoder, threading= None, puncpat='11')
        self.epy_block_2 = epy_block_2.rsa_encrypt_byte(public_e=65537, n=253)
        self.epy_block_1_0 = epy_block_1_0.opus_encoder_stream(sample_rate=48000, bitrate=64000)
        self.digital_protocol_formatter_bb_0_0 = digital.protocol_formatter_bb(hdr, 'packet_len')
        self.digital_crc32_bb_0_0 = digital.crc32_bb(False, "packet_len", True)
        self.digital_constellation_modulator_0_0 = digital.generic_mod(
            constellation=qpsk,
            differential=True,
            samples_per_symbol=sps,
            pre_diff_code=True,
            excess_bw=excess_bw,
            verbose=False,
            log=False,
            truncate=False)
        self.digital_additive_scrambler_xx_0 = digital.additive_scrambler_bb(0x8A, 0x7F, 8, count=0, bits_per_byte=3, reset_tag_key="")
        self.blocks_unpack_k_bits_bb_1_0_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_tagged_stream_mux_0_0_0 = blocks.tagged_stream_mux(gr.sizeof_char*1, 'packet_len', 0)
        self.blocks_stream_to_tagged_stream_0_0_0_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, payload_size, "packet_len")
        self.blocks_pack_k_bits_bb_0_0_0 = blocks.pack_k_bits_bb(8)
        self.blocks_matrix_interleaver_0 = blocks.matrix_interleaver(
            itemsize=gr.sizeof_char * 1, rows=32, cols=80, deint=False
        )
        self.audio_source_0 = audio.source(samp_rate, '', True)
        self.audio_source_0.set_max_output_buffer(16384)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.audio_source_0, 0), (self.epy_block_1_0, 0))
        self.connect((self.audio_source_0, 0), (self.qtgui_time_sink_x_1_1_0_0_0, 0))
        self.connect((self.blocks_matrix_interleaver_0, 0), (self.blocks_pack_k_bits_bb_0_0_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0_0_0, 0), (self.blocks_stream_to_tagged_stream_0_0_0_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0_0_0_0, 0), (self.digital_crc32_bb_0_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0_0_0, 0), (self.digital_constellation_modulator_0_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_1_0_0, 0), (self.fec_extended_encoder_0, 0))
        self.connect((self.digital_additive_scrambler_xx_0, 0), (self.blocks_unpack_k_bits_bb_1_0_0, 0))
        self.connect((self.digital_constellation_modulator_0_0, 0), (self.filter_fft_rrc_filter_0_1, 0))
        self.connect((self.digital_constellation_modulator_0_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.digital_crc32_bb_0_0, 0), (self.blocks_tagged_stream_mux_0_0_0, 1))
        self.connect((self.digital_crc32_bb_0_0, 0), (self.digital_protocol_formatter_bb_0_0, 0))
        self.connect((self.digital_protocol_formatter_bb_0_0, 0), (self.blocks_tagged_stream_mux_0_0_0, 0))
        self.connect((self.epy_block_1_0, 0), (self.epy_block_2, 0))
        self.connect((self.epy_block_2, 0), (self.digital_additive_scrambler_xx_0, 0))
        self.connect((self.fec_extended_encoder_0, 0), (self.blocks_matrix_interleaver_0, 0))
        self.connect((self.filter_fft_rrc_filter_0_1, 0), (self.iio_pluto_sink_0_0, 0))
        self.connect((self.filter_fft_rrc_filter_0_1, 0), (self.qtgui_freq_sink_x_0, 1))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "RADIO_TX")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_qpsk(self):
        return self.qpsk

    def set_qpsk(self, qpsk):
        self.qpsk = qpsk

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.filter_fft_rrc_filter_0_1.set_taps(firdes.root_raised_cosine(1, 300000, (300000/4), self.excess_bw, (self.sps*25)))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_phase_bw(self):
        return self.phase_bw

    def set_phase_bw(self, phase_bw):
        self.phase_bw = phase_bw

    def get_payload_size(self):
        return self.payload_size

    def set_payload_size(self, payload_size):
        self.payload_size = payload_size
        self.blocks_stream_to_tagged_stream_0_0_0_0.set_packet_len(self.payload_size)
        self.blocks_stream_to_tagged_stream_0_0_0_0.set_packet_len_pmt(self.payload_size)

    def get_hdr(self):
        return self.hdr

    def set_hdr(self, hdr):
        self.hdr = hdr
        self.digital_protocol_formatter_bb_0_0.set_header_format(self.hdr)

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw
        self.filter_fft_rrc_filter_0_1.set_taps(firdes.root_raised_cosine(1, 300000, (300000/4), self.excess_bw, (self.sps*25)))

    def get_encoder(self):
        return self.encoder

    def set_encoder(self, encoder):
        self.encoder = encoder

    def get_cma_algo(self):
        return self.cma_algo

    def set_cma_algo(self, cma_algo):
        self.cma_algo = cma_algo




def main(top_block_cls=RADIO_TX, options=None):

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
