import sys
import os.path
import pandas as pd

class CsvCombiner:
    
    #Checks to see if users command and its file paths are valid
    #argv: input arguments
    #return: true if all arguments are valid
    @staticmethod
    def correctFilePaths(argv):

        if len(argv) <= 1:
            print("Must have MORE THAN 2 inputs. Example: \n" + 
                  "python3 ./csvcombiner.php ./fixtures/accessories.csv ./fixtures/clothing.csv > combined.csv")
            return False
        
        filelist = argv[1:]

        for  filepath in filelist:
            if not os.path.exists(filepath):
                print("File is not found!")
                return False
            if os.stat(filepath).st_size == 0:
                print("Warning: The following file is empty: " + filepath)
                return False
        return True

    #Prints rows to stdout in csv files and then combines them.
    def comboFiles(self, argv):
        
        chunksize = 10 ** 6
        chunklist = []

        if self.correctFilePaths(argv):
            filelist = argv[1:]
            
            for Filepath in filelist:
                #Optimizing memory to prevent memory problems
                for chunk in pd.read_csv(Filepath, chunksize=chunksize):

                    #getting file name from path
                    filename = os.path.basename(Filepath)

                    #putting filename into the chunk
                    chunk['filename'] = filename
                    chunklist.append(chunk)
            
            #checking to see if a header is needed
            header = True

            #combining the chunks which both csv files are in
            for chunk in chunklist:
                print(chunk.to_csv(index=False, header=header, lineterminator='\n', chunksize=chunksize), end='')
                header = False
        else:
            return
    
def main():
    combiner = CsvCombiner()
    combiner.comboFiles(sys.argv)

if __name__ == '__main__':
    main()






