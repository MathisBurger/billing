from PyPDF2 import PdfReader, PdfFileWriter

bwa = PdfReader(open("data/068-BWA.pdf"))
abrg = PdfReader(open("data/068-Abrg..pdf"))
coverLetter = PdfReader(open("data/068-Anschreiben.pdf"))
bew = PdfReader(open("data/068-HD Bew..pdf"))
egt = PdfReader(open("data/068-HD Egt..pdf"))