"""Design §3.8 CLI; the parent sphere mask and sphere-C tail at every requested height."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from ringeval_uvt_c2v003 import main
if __name__=='__main__':main('sphere')
