from PyPDF2 import PdfReader, PdfWriter

# Adds all documents to pdf writer object
def add_to_doc(output, data):
    for i in range(len(data)):
        output.add_page(data[i])
    return output

# Finds all entries in a pdf by a specific key word
# and arranges them in a two dimensional array
def find_entries(keyword, pages):
    entries = []
    for i in range(len(pages)):
        content = pages[i].extract_text()
        if keyword in content:
            entries.append([pages[i]])
        else:
            entries[len(entries)-1].append(pages[i])
    return entries


# Init PDF readers of all documents
bwa = PdfReader(open(input("BWA Pfad:"), "rb"))
abrg = PdfReader(open(input("ABRG Pfad:"), "rb"))
coverLetter = PdfReader(open(input("Abschreiben Pfad:"), "rb"))
bew = PdfReader(open(input("BEW Pfad:"), "rb"))
egt = PdfReader(open(input("EGT Pfad:"), "rb"))

# All arranged entries in their two dimensional arrays
# with excactly the same length
abrgEntries = find_entries("1. Einzelabrechnung", abrg.pages)
print("ABRG: " + len(abrgEntries))
coverLetterEntries = find_entries("Jahresabrechnung", coverLetter.pages)
print("Anschreiben: " + len(coverLetterEntries))
bewEntries = find_entries("Anlage zur Jahresabrechnung für den Zeitraum", bew.pages)
print("BEW: " + len(bewEntries))
egtEntries = find_entries("Anlage zur Jahresabrechnung für den Zeitraum", egt.pages)
print("EGT: " + len(egtEntries))

# Generates all output PDFs
sub = input("Dateiname:")
for i in range(len(abrgEntries)):
    output = PdfWriter()
    with_cover = add_to_doc(output, coverLetterEntries[i])
    with_bwa = add_to_doc(with_cover, bwa.pages)
    with_abrg = add_to_doc(with_bwa, abrgEntries[i])
    with_bew = add_to_doc(with_abrg, bewEntries[i])
    with_egt = add_to_doc(with_bew, egtEntries[i])
    with open(f"{sub}-{i+1}.pdf", "wb") as outputStream:
        output.write(outputStream)