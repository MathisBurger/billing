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

# Default runner that is executed to process all PDF files
# that are provided
def default_runner(bwa_path, abrg_path, coverLetter_path, bew_path, egt_path, journal_path, rl_path, vb_path, wp_einzel_path, sonstige_path, sub):

    # Init PDF readers of all documents
    bwa = PdfReader(open(bwa_path, "rb"))
    abrg = PdfReader(open(abrg_path, "rb"))
    coverLetter = PdfReader(open(coverLetter_path, "rb"))
    bew = PdfReader(open(bew_path, "rb"))
    egt = PdfReader(open(egt_path, "rb"))
    journal = PdfReader(open(journal_path, "rb"))
    rl = PdfReader(open(rl_path, "rb"))
    vb = PdfReader(open(vb_path, "rb"))
    wp_einzel = PdfReader(open(wp_einzel_path, "rb"))

    # Adds other documents that are not specificed
    sonst_pages = []
    try:
        sonst_pages = PdfReader(open(sonstige_path, "rb")).pages
    except:
        pass

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
    wpEinzelEntries = find_entries("Wirtschaftsplan für das Wirtschaftsjahr", wp_einzel.pages)
    print("WP Einzel: " + str(len(egtEntries)))

    # Generates all output PDFs
    for i in range(len(abrgEntries)):
        output = PdfWriter()
        add_to_doc(output, coverLetterEntries[i])
        add_to_doc(output, bwa.pages)
        add_to_doc(output, abrgEntries[i])
        add_to_doc(output, bewEntries[i])
        add_to_doc(output, egtEntries[i])
        add_to_doc(output, wpEinzelEntries[i])
        add_to_doc(output, journal.pages)
        add_to_doc(output, rl.pages)
        add_to_doc(output, vb.pages)
        add_to_doc(output, sonst_pages)
        with open(f"{sub}-{i+1}.pdf", "wb") as outputStream:
            output.write(outputStream)
    print("Done!")