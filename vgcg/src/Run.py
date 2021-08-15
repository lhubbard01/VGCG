FOR_BATCH    = "for b, (d,t) in enumerate(dlTr):"
FOR_EPOCH    = "for epoch in range(epochs):"
DATA_TO_1D   = "d = d[:].reshape(1,-1)"
DATA_TO_CUDA = "d, t = d.cuda(), t.cuda()"
CRITERION    = "criterion({}, {}"
VALIDATION   = "for bval, (dval, tval) in enumerate(dlVal):"
OPT_STEP     = "{}.step()"
OPT_ZERO     = "{}.zero_grad()"

