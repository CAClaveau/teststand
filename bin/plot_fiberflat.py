#!/usr/bin/env python

import numpy as np
import astropy.io.fits as fits
import pylab
import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-f','--fiberflat', type = str, default = None, required = True,
                    help = 'path to fiber flat file')

args        = parser.parse_args()
h=fits.open(args.fiberflat)


h.info()

wave=h["WAVELENGTH"].data
#meanspec=np.mean(h[0].data,axis=0)
meanspec=np.ones((h[0].data.shape[1]))
ratio=h[0].data/meanspec
ivar=h[1].data*meanspec**2

wrebin=100
rwave=wave[:(wave.size/wrebin)*wrebin].reshape((wave.size/wrebin),wrebin).mean(-1)

fbin=50
nfbin=500/fbin
for f in np.arange(0,nfbin) :
    color=pylab.cm.rainbow(f/float(nfbin))
    mratio=np.mean(ratio[fbin*f:fbin*(f+1)],axis=0)
    mivar=np.sum(ivar[fbin*f:fbin*(f+1)],axis=0)
    rmratio=mratio[:(wave.size/wrebin)*wrebin].reshape((wave.size/wrebin),wrebin).mean(-1)
    rmivar=mivar[:(wave.size/wrebin)*wrebin].reshape((wave.size/wrebin),wrebin).sum(-1)
    err=1./np.sqrt(rmivar)
    pylab.fill_between(rwave,rmratio-1-err,rmratio-1+err,color=color,alpha=0.2)
    pylab.plot(rwave,rmratio-1,c=color,lw=2)
pylab.xlabel("wavelength (A)")
pylab.ylabel("fiber flat syst. error")
pylab.grid()    
pylab.show()
