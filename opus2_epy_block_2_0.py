import numpy as np
from gnuradio import gr

class rsa_decrypt_byte(gr.sync_block):
    def __init__(self, private_d=63, n=253):
        gr.sync_block.__init__(
            self,
            name='RSA Decryption',
            in_sig=[np.uint8],
            out_sig=[np.uint8]
        )
        self.d = private_d
        self.n = n

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        
        # RSA Decryption: m = (c^d) % n
        for i in range(len(in0)):
            out[i] = pow(int(in0[i]), self.d, self.n)
            
        return len(output_items[0])