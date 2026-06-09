from django.http import FileResponse, HttpResponse

from .models import Member
from .pdf_generator import build_member_pdf


def generate_member_pdf(request, pk):
    try:
        member = Member.objects.get(id=pk)
    except Member.DoesNotExist:
        return HttpResponse("Member Not Found", status=404)

    pdf_buffer = build_member_pdf(member)
    pdf_buffer.seek(0)

    return FileResponse(
        pdf_buffer,
        as_attachment=True,
        filename=f"{member.full_name}.pdf",
        content_type="application/pdf"
    )

