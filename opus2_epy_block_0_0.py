import numpy as np
from gnuradio import gr
import opuslib

class opus_decoder_stream(gr.basic_block):
    def __init__(self, sample_rate=48000):
        gr.basic_block.__init__(self, name='Opus Decoder Stream',
                                in_sig=[np.uint8], out_sig=[np.float32])
        
        self.sample_rate = sample_rate
        self.frame_size = 960 
        self.dec = opuslib.Decoder(sample_rate, 1)

    def general_work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        
        # 1. Scan for Sync Word (0xAA 0x55)
        sync_idx = -1
        for i in range(len(in0) - 1):
            if in0[i] == 0xAA and in0[i+1] == 0x55:
                sync_idx = i
                break

        if sync_idx == -1:
            # Sync not found. Consume everything except the last byte 
            # (in case it is 0xAA and the 0x55 is in the next buffer)
            consume_len = max(0, len(in0) - 1)
            if consume_len > 0:
                self.consume(0, consume_len)
            return 0

        # 2. If sync word isn't at the very beginning, consume the garbage before it
        if sync_idx > 0:
            self.consume(0, sync_idx)
            return 0 # Return to realign the buffer on the next call

        # 3. Read Length Header
        if len(in0) < 4:
            return 0 # Wait for length bytes
            
        packet_len = (int(in0[2]) << 8) | int(in0[3])
        total_len = packet_len + 4
        
        # 4. Wait for full packet and output space
        if len(in0) < total_len:
            return 0 
            
        if len(out) < self.frame_size:
            return 0 
            
        packet_data = bytes(in0[4:total_len])
        
        try:
            # 5. Decode Audio
            decoded_pcm = self.dec.decode(packet_data, self.frame_size)
            floats = np.frombuffer(decoded_pcm, dtype=np.int16).astype(np.float32) / 32767.0
            
            out[:self.frame_size] = floats
            self.consume(0, total_len)
            return self.frame_size
            
        except Exception as e:
            # Decode failed (could be a false sync word or corrupted payload).
            # Consume the 0xAA 0x55 so we don't get stuck in an infinite loop, and resume searching.
            self.consume(0, 2)
            return 0