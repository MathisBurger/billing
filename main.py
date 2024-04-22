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


def default_runner(bwa_path, abrg_path, coverLetter_path, bew_path, egt_path, sub):
    # Init PDF readers of all documents
    bwa = PdfReader(open(bwa_path, "rb"))
    abrg = PdfReader(open(abrg_path, "rb"))
    coverLetter = PdfReader(open(coverLetter_path, "rb"))
    bew = PdfReader(open(bew_path, "rb"))
    egt = PdfReader(open(egt_path, "rb"))
    print("")

    # All arranged entries in their two dimensional arrays
    # with excactly the same length
    abrgEntries = find_entries("1. Einzelabrechnung", abrg.pages)
    print("ABRG: " + str(len(abrgEntries)))
    coverLetterEntries = find_entries("Jahresabrechnung", coverLetter.pages)
    print("Anschreiben: " + str(len(coverLetterEntries)))
    bewEntries = find_entries("Anlage zur Jahresabrechnung für den Zeitraum", bew.pages)
    print("BEW: " + str(len(bewEntries)))
    egtEntries = find_entries("Anlage zur Jahresabrechnung für den Zeitraum", egt.pages)
    print("EGT: " + str(len(egtEntries)))

    # Generates all output PDFs
    print("")
    for i in range(len(abrgEntries)):
        output = PdfWriter()
        with_cover = add_to_doc(output, coverLetterEntries[i])
        with_bwa = add_to_doc(with_cover, bwa.pages)
        with_abrg = add_to_doc(with_bwa, abrgEntries[i])
        with_bew = add_to_doc(with_abrg, bewEntries[i])
        with_egt = add_to_doc(with_bew, egtEntries[i])
        with open(f"{sub}-{i+1}.pdf", "wb") as outputStream:
            output.write(outputStream)
    print("Done!")

#bwa = input("BWA Pfad: ")
#abrg = input("ABRG Pfad: ")
#coverLetter = input("Anschreiben Pfad: ")
#bew = input("BEW Pfad: ")
#egt = input("EGT Pfad: ")
#sub = input("Dateiname:")