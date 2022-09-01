# python-file-transfer
## Two simple Python programs, a file generator source and a server to receive them.

Workflow or File Flow

 

Source Folder:

This folder receives files from a generator every 2 seconds.

The filenames are Vx.mp4, Ax.mp4, where x is incremented by 1 every 2 sec in that order.

Another file mpdFile.xml is generated that contains the filenames Vx.mp4 and Ax.mp4

Then another file, Cx.xml is received after every 6 mins. The mpdFile.xml is updated with Vx.mp4, Ax.mp4 and Cx.xml files.

Files lifetime in the source folder is 10 sec

mpdFile.xml does not change the name, it only updates the contents after the files Vx.mp4, Ax.mp4 and Cx.xml are received

 

Destination Folder:

This folder is a remote server which will receive the file in the /downloads/newUploads directory where /newUploads directory is a directory name of your choosing.

The same destination folder will be full if the files which were copied are not deleted thus, a HTTP DELETE is sent after 10 sec once the file is sent thus, cleaning the directory of the used file

 

For simplicity, the assessment is for copying files from a local source folder to a local destination folder using HTTP PUT protocol only, and since you mentioned web access, using port 8081.

 

The tasks:

 

Optional: Create a source File generator for Vx,mp4, Ax.mp4 mpdFile.xml every 2 second and move the files to source folder. Then, create another file Cx.xml every after 6 mins and moved to the source folder.

 

Create a source folder that will receive the files from the File Generator

Create a Destination folder that will receive the files from the source folder using HTTP PUT protocol and OPTIONAL: delete the files that were receive for the lifetime of 10 sec.
