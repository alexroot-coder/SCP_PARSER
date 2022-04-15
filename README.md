# SCP_PARSER  
SCP_PARSER  
INSTALL:  
pip install -r requirements.txt  
pip install pdfkit  
wkhtmltopdf.exe https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_msvc2015-win64.exe  
  
Usage: scp_parser.py [options]  

Options:  
\t-h, --help            show this help message and exit  
  -b BIG_ONE, --big_one=BIG_ONE  
                        1 - true, 0 - false  
  -s SCP_NAME, --scp_name=SCP_NAME  
                        scp-name >> http://scpfoundation.net  
  -n NUMBER_START, --number_start=NUMBER_START  
                        number to start parse  
  -N NUMBER_FINISH, --number_finish=NUMBER_FINISH  
                        number to finish parse  
