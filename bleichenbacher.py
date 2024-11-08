
class Bleichenbacher:


  def __init__(self, N, e):
    self.N = N
    self.e = e

  def power(A, B, N):
    val = 1
    while B > 0:
      if (B & 1) > 0:
        val = (val * A) % N
      A = (A * A) % N
      B >>= 1
    return val

  def ceil(self,A,B):
    return (A + B - 1)//B

  def floor(self,A,B):
    return int(A // B)

  def find_first_s(self, minVal, ctxt, oracle):
    s = minVal
    while True:
      mod_ctxt = (ctxt * self.power(s, self.e, self.N)) % self.N
      if oracle(mod_ctxt):
          return s
      s += 1
      #print('i can run forever!!1')
  
  def find_bounded_s(self,a,b,prev_s,B,ctxt,oracle):
      r = 2 * self.ceil((b * prev_s) - (4 * B),self.N)
      while True:
          min_numerator = (4 * B) + (r * self.N)
          s_min = self.ceil(min_numerator,b)
          max_numerator = (5 * B) + (r * self.N)
          s_max = self.ceil(max_numerator,a)
          for s in range(s_min, s_max):
              mod_ctxt = (ctxt * self.power(s, self.e, self.N)) % self.N
              if oracle(mod_ctxt):
                return s
          r = r + 1
          #print('i can run forever!!2')

  def add_block(self,new_M, block):
      counter = 0
      for element in new_M:
          if (element[0] <= block[1]) and (element[1] >= block[0]):
              newA = min(element[0],block[0])
              newB = max(element[1],block[1])
              if newA <= newB:
                new_M[counter] = block
                return new_M
      new_M.append(block)
      return new_M


  def create_new_M(self,M,s,B):
      new_M = []
      for ele in M:
          min_numerator = (ele[0] * s) - (5 * B) +1
          r_min = self.ceil(min_numerator,self.N)
          max_numerator = (ele[1] * s) - (4 * B)
          r_max = self.ceil(max_numerator,self.N)
          for r in range(r_min,r_max):
              low_numerator = (4 * B) + (r * self.N)
              low = max(ele[0], self.ceil(low_numerator,s))
              upr_numerator = (5 * B) - 1 + (r * self.N)
              upr = min(ele[1], self.ceil(upr_numerator,s))
              block = [low,upr]
              new_M = self.add_block(new_M,block)
      return new_M
  def decrypt(self, ctxt, oracle):
    k = ((self.N.bit_length() + 8 - 1) // 8)
    #print(k)
    expo = 8 * (k - 2)
    B = pow(2,expo)
    M =[ [4 * B , 5 * B - 1] ]
    s = self.find_first_s(self.ceil(self.N,(5*B)),ctxt,oracle)
    M = self.create_new_M(M,s,B)
    while True:
        if len(M) == 1:
            a = M[0][0]
            b = M[0][1]
            if a == b:
                return a - 1
            s = self.find_bounded_s(a,b,s,B,ctxt,oracle)
        else:
            #print('st2')
            s = self.find_first_s(s + 1,ctxt,oracle)
        M = self.create_new_M(M, s, B)
    return 0
