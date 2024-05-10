
import os
import glob
import subprocess  
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

import pickle 
pdflatex_path = 'C:/Users/aleja/AppData/Local/Programs/MiKTeX/miktex/bin/x64' 
os.environ["PATH"] += os.pathsep + pdflatex_path

def svg_to_pdf(svg_file, pdf_file):
    """Convert SVG image to PDF"""
    drawing = svg2rlg(svg_file)
    renderPDF.drawToFile(drawing, pdf_file)


def create_tex_report(directory, photo_directory, peaks_dict, image_scale=0.3):  # Adjust image_scale to 0.7
    """Create a LaTeX report with images in the directory"""
    images = sorted(glob.glob(os.path.join(directory, '*.svg')))
    photos = sorted(glob.glob(os.path.join(photo_directory, '*.JPG')))

    for i, image in enumerate(images):
        pdf_image = os.path.splitext(image)[0] + '.pdf'
        svg_to_pdf(image, pdf_image)

    with open('report.tex', 'w') as f:
        f.write("\\documentclass{article}\n")
        f.write("\\usepackage{graphicx}\n")
        f.write("\\usepackage{tabularx}\n")
        f.write("\\usepackage[landscape, top=2 in, bottom=0.2 in, left=0.2 in, right=0.2 in, papersize={21.59 cm, 27.94 cm}]{geometry}\n")
        f.write("\\usepackage[export]{adjustbox}\n")  # Add package to adjust the box
        f.write("\\usepackage{fancyhdr}\n")  # For headers and footers
        f.write("\\usepackage{lastpage}\n")  # For page number
        f.write("\\usepackage{datetime}\n")  # For current date
        f.write("\\usepackage{multirow}\n")

        f.write("\\pagestyle{fancy}\n")
        f.write("\\fancyhf{}\n")  # Clear all header and footer fields
        f.write("\\renewcommand{\\headrulewidth}{0pt}\n")  # No decorative line+
        


        # Add table with revision information
        f.write("\\fancyhead[C]{\\\ \n")
        f.write("\\begin{tabular}{ccc}\n")
        f.write("\\multirow{2}{*}{\\includegraphics[width=3cm]{Gold Logo Black Text Transparent.png}} & Vibration Assessment Centrifuges & Rev 0 \\\\\n")
        f.write(" & \\today & \\\\\n ")
        f.write("\\end{tabular}}\n")
        f.write("\\begin{document}\n")


        

        for i in range(len(images)):
            centri_name = 'centri_md_' + os.path.splitext(os.path.basename(photos[i]))[0][-1]
            f.write("\\begin{center}\n")  # Center the table
            f.write("\\begin{tabular*}{0.6\\textwidth}{@{\\extracolsep{\\fill}}cc}\n")  # Change to tabular* and adjust column specification

            # Include the SVG image
            pdf_image = os.path.splitext(images[i])[0] + '.pdf'
            pdf_image = pdf_image.replace('\\', '/')
            f.write("\\includegraphics[width=" + str(image_scale) + "\\linewidth, valign=c]{" + pdf_image + "} &\n")  # Add scale variable

            # Include the photo
            photo_image = photos[i]
            photo_image = photo_image.replace('\\', '/')
            f.write("\\includegraphics[width=" + str(image_scale) + "\\linewidth, valign=c]{" + photo_image + "} \\\\\n")  # Add scale variable
            
            # Include the text
            peaks = peaks_dict[centri_name]
            text = f"A vibration assessment was carried out in the following centrifuges measuring acceleration above the vibration dampers and in the supporting structure (after the vibration dampers), the following frequencies were identified: {peaks[0]} Hz.\n"
            f.write("\\multicolumn{2}{|p{0.6\\textwidth}|}{" + text + "} \\\\\n")  # Adjust text width to match table width

            f.write("\\end{tabular*}\n")
            f.write("\\end{center}\n")  # End centering
            
            f.write("\\newpage\n")


        f.write("\\end{document}\n")


def compile_tex_to_pdf(tex_file):
    """Compile the LaTeX report into a PDF"""
    directory = os.getcwd() # use the current directory
    base_name = os.path.splitext(os.path.basename(tex_file))[0]
    latex_command = ['pdflatex', '-interaction=nonstopmode', base_name + '.tex']
    print("Latex command: ", latex_command)  # Debug line
    print("Working directory: ", directory)  # Debug line
    try:
        output = subprocess.check_output(latex_command, cwd=directory)
        print(output)
    except subprocess.CalledProcessError as e:
        print("pdflatex command failed with return code", e.returncode)
        print(e.output)

# Load the peaks data
with open('peaks.pickle', 'rb') as handle:
    peaks_dict = pickle.load(handle)

# Specify the directory with your SVG images and photos
image_directory = '.'
photo_directory = './centri_photos'

# Create the LaTeX report
create_tex_report(image_directory, photo_directory, peaks_dict)

# Compile the LaTeX report to PDF
compile_tex_to_pdf("report.tex")