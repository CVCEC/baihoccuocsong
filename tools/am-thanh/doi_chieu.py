import numpy as np, sys
from scipy.io import wavfile
from scipy.signal import stft
def mel(p):
    sr,x=wavfile.read(p); x=x.astype(float)/32768
    f,t,Z=stft(x,sr,nperseg=512,noverlap=512-320)  # 20 ms
    S=np.abs(Z)**2
    # 24 dải tần log 100–6000 Hz
    ed=np.geomspace(100,6000,25); B=np.stack([S[(f>=ed[i])&(f<ed[i+1])].sum(0) for i in range(24)])
    L=np.log(B+1e-8); L=L-L.mean(1,keepdims=True)
    return L.T
def ban_do(old,new,W=100,step=25,R=1500):
    A=mel(old); B=mel(new); out=[]
    for i in range(0,len(B)-W,step):
        b=B[i:i+W]
        if np.abs(b).sum()==0: continue
        lo=max(0,i-R); hi=min(len(A)-W,i+R)
        best=None
        bn=(b-b.mean())/(b.std()+1e-9)
        # tìm lệch tốt nhất bằng tương quan
        sc=[]
        for j in range(lo,hi,2):
            a=A[j:j+W]; an=(a-a.mean())/(a.std()+1e-9); sc.append(((an*bn).mean(),j))
        s,j=max(sc); out.append((i*0.02,(j-i)*0.02,s))
    return out
if __name__=='__main__':
    k=int(sys.argv[1])
    for t,d,s in ban_do(f'/home/claude/lensau/wav/kho{k:02d}.wav',f'wav/kho{k:02d}.wav'):
        print(f"{t:6.1f} lệch {d:+6.2f} r={s:.2f}")
