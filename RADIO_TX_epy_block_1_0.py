import numpy as np
from gnuradio import gr
import opuslib

class opus_encoder_stream(gr.basic_block):
    def __init__(self, sample_rate=48000, bitrate=64000):
        gr.basic_block.__init__(self, name='Opus Encoder Stream',
                                in_sig=[np.float32], out_sig=[np.uint8])
        
        self.sample_rate = sample_rate
        self.frame_size = 960 
        self.enc = opuslib.Encoder(sample_rate, 1, 'audio')
        self.enc.bitrate = bitrate

    def general_work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        
        if len(in0) < self.frame_size:
            return 0
            
        chunk = (in0[:self.frame_size] * 32767).astype(np.int16)
        
        try:
            encoded_packet = self.enc.encode(chunk.tobytes(), self.frame_size)
            packet_len = len(encoded_packet)
            total_len = packet_len + 4 # 2 bytes sync + 2 bytes length
            
            if len(out) < total_len:
                return 0
                
            # 1. Write Sync Word (0xAA 0x55)
            out[0] = 0xAA
            out[1] = 0x55
            
            # 2. Write 2-byte length header
            out[2] = (packet_len >> 8) & 0xFF
            out[3] = packet_len & 0xFF
            
            # 3. Write payload
            out[4:total_len] = np.frombuffer(encoded_packet, dtype=np.uint8)
            
            self.consume(0, self.frame_size)
            return total_len
            
        except Exception as e:
            print(f"Encode error: {e}")
            self.consume(0, self.frame_size)
            return 0