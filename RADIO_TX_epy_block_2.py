import numpy as np
from gnuradio import gr

class rsa_encrypt_byte(gr.sync_block):
    def __init__(self, public_e=7, n=253):
        gr.sync_block.__init__(
            self,
            name='RSA Encryption',
            in_sig=[np.uint8],
            out_sig=[np.uint8]
        )
        self.e = public_e
        self.n = n

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        
        # RSA Encryption: c = (m^e) % n
        # We use pow(m, e, n) for efficient modular exponentiation
        for i in range(len(in0)):
            if in0[i] >= self.n:
                # Value too high for this small modulus, clip it
                val = self.n - 1
            else:
                val = in0[i]
            
            out[i] = pow(int(val), self.e, self.n)
            
        return len(output_items[0])