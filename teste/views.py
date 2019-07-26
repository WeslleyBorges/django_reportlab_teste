from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template.loader import render_to_string
from django.views.generic import ListView
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle, Image

from teste.models import Teste
import io
from reportlab.pdfgen import canvas


class UserListView(ListView):
    model = Teste
    template_name = 'teste/teste.html'  # Default: <app_label>/<model_name>_list.html
    context_object_name = 'users'  # Default: object_list
    paginate_by = 10
    queryset = Teste.objects.all()  # Default: Model.objects.all()


def write_pdf_view(request):
    doc = SimpleDocTemplate("/tmp/somefilename.pdf")

    styles = getSampleStyleSheet()
    story = [Spacer(1, 2 * inch)]
    style = styles["Normal"]

    for i in range(100):
       bogustext = ("This is Paragraph number %s.  " % i) * 20

       from reportlab.platypus import Paragraph

       p = Paragraph(bogustext, style)

       story.append(p)
       story.append(Spacer(1, 0.2*inch))

    doc.build(story)

    fs = FileSystemStorage("/tmp")
    with fs.open("somefilename.pdf") as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
        return response

    return response


def pdf_table_test(request):
    doc_name = 'simple_table.pdf'
    doc = SimpleDocTemplate(doc_name, pagesize=letter)

    # container for the 'Flowable' objects
    elements = []

    logo = Image('zed-classic.png')
    logo.drawHeight = 1.25 * inch * logo.drawHeight / logo.drawWidth
    logo.drawWidth = 1.25 * inch

    data = [['00', '01', '02', '03', '04'],
            ['10', '11', '12', logo, '14'],
            ['20', '21', '22', '23', '24'],
            ['30', '31', '32', '33', '34']]
    t = Table(data)
    t.setStyle(TableStyle([('BACKGROUND', (1, 1), (-2, -2), colors.green),
                           ('TEXTCOLOR', (0, 0), (1, -1), colors.red)]))
    elements.append(t)

    # write the document to disk
    doc.build(elements)

    fs = FileSystemStorage()

    with fs.open(doc_name) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=' + doc_name
        return response

    return response


def my_own_grid(request):
    doc_name = 'lorem_ipsum_grid.pdf'
    doc = SimpleDocTemplate(doc_name, pagesize=letter)

    building = []

    data = []

    logo = Image('zed-classic.png')
    logo.drawHeight = 1.25 * inch * logo.drawHeight / logo.drawWidth
    logo.drawWidth = 1.25 * inch

    report_header = [logo, None]

    data.append(report_header)

    cols_header = ['ID', 'Descrição']

    data.append(cols_header)

    for t in Teste.objects.all():
        data.append([t.pk, t.descricao])

    table = Table(data)

    color_style = [('SPAN', (0, 0), (-1, 0)),
                   ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                   ('BOX', (0, 0), (-1, -1), 1, colors.black),
                   ('INNERGRID', (0, 0), (-1, -1), 1, colors.black)]

    table.setStyle(TableStyle(color_style))

    building.append(table)

    doc.build(building)

    fs = FileSystemStorage()

    with fs.open(doc_name) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=' + doc_name
        return response

    return response


def pdf_lorem_ipsum(request):
    doc_name = 'lorem_ipsum.pdf'
    doc = SimpleDocTemplate(doc_name, pagesize=letter)
    # container for the 'Flowable' objects
    elements = []

    data = [['ID', 'Palavra']]

    for t in Teste.objects.all():
        data.append([t.pk, t.descricao])

    t = Table(data)

    # Style para os headers
    t.setStyle(TableStyle([('BOX', (0, 0), (1, 1), 0.25, colors.black)]))

    t.setStyle(TableStyle([('TEXTCOLOR', (0, 0), (1, -1), colors.red),
                           ('BOX', (0, 0), (-1, -1), 0.25, colors.black),

                           ('TEXTCOLOR', (1, 1), (-2, -2), colors.red),
                           ('TEXTCOLOR', (0, 0), (0, -1), colors.blue),
                           ('TEXTCOLOR', (0, 0), (-1, -1), colors.green),

                           ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),

                           ('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                           ('VALIGN', (0, 0), (0, -1), 'TOP'),
                           ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                           ('VALIGN', (0, -1), (-1, -1), 'MIDDLE')]))
    elements.append(t)

    # write the document to disk
    doc.build(elements)

    fs = FileSystemStorage()

    with fs.open(doc_name) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=' + doc_name
        return response

    return response


def pdf_test(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    return FileResponse(buffer, filename='hello.pdf')