import os
import subprocess

def shellcmd(cmd, verbose = False):

    process = subprocess.Popen(
        cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True,
        shell = True
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)
    pass



def wget(url, output_dir=None,options="",verbose = True):
    
    if output_dir is not None:
            
            
        if " -O" in options or "--output-document" in options:
            
            raise Exception("The output_fir arguments uses the comand option of ''-O'"
                            " of wget but you specified it in the options"
                           )
            
            
        file_name = os.path.basename(url)
        
        os.makedirs(output_dir,exist_ok=True)
        output_file = os.path.join(output_dir,file_name)
        
        options += f' --output-document="{output_file}"'
        
        
        
    cmd = f"wget {url} {options}"
    shellcmd(cmd,verbose=verbose)
    
