from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_sample_contract(filename="sample_equipment_lease.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    
    # Page 1: Scope & Penalties
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "HEAVY EQUIPMENT LEASE & SERVICE AGREEMENT")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 720, "1. PARTIES & SCOPE OF ENGAGEMENT")
    c.setFont("Helvetica", 10)
    c.drawString(50, 700, "This Agreement is entered into by Titan Industrial Plant Ltd ('Lessor') and Metro EPC Ltd ('Lessee').")
    c.drawString(50, 680, "Lessor agrees to mobilize two 50-Ton Crawler Cranes to Site Sector-4 for 6 months.")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 640, "2. DELIVERY TIMELINES & DELAY PENALTIES")
    c.setFont("Helvetica", 10)
    c.drawString(50, 620, "Equipment mobilization must be completed within 14 calendar days from signing.")
    c.drawString(50, 600, "Liquidated Damages Clause: Failure to mobilize by Day 14 incurs a penalty of INR 25,000 per day")
    c.drawString(50, 580, "capped at a maximum penalty of 10% of the total monthly lease fee.")
    
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(50, 50, "Page 1 of 2 - Confidential Commercial Document")
    c.showPage()
    
    # Page 2: Payment & Termination
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 750, "SCHEDULE B: PAYMENT TERMS & TERMINATION")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 710, "3. INVOICING & MILESTONES")
    c.setFont("Helvetica", 10)
    c.drawString(50, 690, "Monthly lease rate per crane: INR 3,50,000 plus applicable taxes.")
    c.drawString(50, 670, "Invoices must be cleared within 30 days of submission. Overdue interest is charged at 1.5% per month.")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 630, "4. EARLY TERMINATION CLAUSE")
    c.setFont("Helvetica", 10)
    c.drawString(50, 610, "Lessee may terminate this contract by providing 30 days written notice.")
    c.drawString(50, 590, "If terminated without cause before 3 months, Lessee pays a severance compensation of INR 2,00,000.")
    
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(50, 50, "Page 2 of 2 - Confidential Commercial Document")
    c.showPage()
    
    c.save()
    print(f"Generated: {filename}")

if __name__ == "__main__":
    generate_sample_contract()