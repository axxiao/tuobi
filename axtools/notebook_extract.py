import io, os, sys, types,getopt
import IPython
from IPython.core.interactiveshell import InteractiveShell
from nbformat import read
"""
The flag to control if to output the info
"""
OUT_FLAG=False
class JupyterNotebookExtract(object):
    """
    The class of extractor 
    
    """
    def __init__(self):
        self.shell=InteractiveShell.instance()
        jupyter=IPython.get_ipython()
        self.base_dir=str(jupyter.home_dir)
        if(OUT_FLAG):
            print('Jupyter Notebook Base Dir:',self.base_dir)
    
    def extract(self,input_filename,output_filename='',inlcude_all=False):
        """
            Convert .ipynb file to .py
            
            input_filename: the input file name (with path, if not absolute, will use jupyter notebook base folder as root)
            output_filename: [Optional] if not set default to same name as inputfile
            inlcude_all: [Optional: default to False] if include none-code sections as comments
    
            Please adjust OUT_FLAG of the package to control if ouput processing info    
        """
        if(OUT_FLAG):
            print('Extract Raw Input file:',input_filename)
            print('Extract Raw Output file:',output_filename)
        input_filename_s=input_filename.strip()
        output_filename_s=output_filename.strip()
        
        if input_filename_s[-6:].lower()!='.ipynb':
            #remove the .ipynb extension
            input_filename_s=input_filename_s+'.ipynb'
            
        if output_filename_s=='' or output_filename_s==None:
            output_filename_s=input_filename_s[:-6]+'.py'
        if output_filename_s[-3:].lower()!='.py':
            #remove the .ipynb extension
            output_filename_s=output_filename_s+'.py'
        
        if os.path.isabs(input_filename):
            #if absoult path
            inputfile=input_filename_s
        else:
            inputfile=os.path.join(self.base_dir, input_filename_s)
            
        if os.path.isabs(output_filename_s):
            #if absoult path
            outfile=output_filename_s
        else:
            outfile=os.path.join(self.base_dir, output_filename_s)
        
                    
        if(OUT_FLAG):
            print('Extract Input file:',inputfile)
            print('Extract Output file:',outfile)
        with io.open(inputfile, 'r', encoding='utf-8') as f:
            nb = read(f, 4)
        with open(outfile,'w') as out:
            for cell in nb.cells:
                code = self.shell.input_transformer_manager.transform_cell(cell.source) 
                if cell.cell_type != 'code' and inlcude_all:
                    code='#'+code.replace('\n','\n#')
                out.write(code)
        if(OUT_FLAG):
            print('Done extracted to',outfile)
        
    
#JupyterNotebookExtract().extract('axtools/import_from_file')
#JupyterNotebookExtract().extract('axtools/notebook_extract')
#JupyterNotebookExtract().extract('/data/tuobi/Server/notebook_extract.ipynb',filename,True)
def main(argv):
    filename='Server/main_web_app'
    helpline='Please use command: \n\t python3 notebook_extract.py -i <inputfile> [-o <outputfile>]'
    helpline+='\n you can either give the relative filename (from home of Jupyter Notebook WITHOUT extensions) or '
    helpline+='you can specify the absoult path WITH extension' 
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["inputfile=","outputfile="])
    except getopt.GetoptError:
        print (helpline)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(helpline)
            sys.exit()
        elif opt in ("-i", "--inputfile"):
            inputfile = arg
        elif opt in ("-o", "--outputfile"):
            outputfile = arg
    JupyterNotebookExtract().extract(inputfile,outputfile,True)
        
if __name__ == "__main__":
    main(sys.argv[1:])
    

