from flask import Flask, render_template, make_response, send_file
import os
import subprocess
from app.models.inventory_models import Inventory
from app.services.services import CRUDService

inventory_service = CRUDService(Inventory)

def receiptGenerate():
   
    item_list = inventory_service.get()
       
    return render_template('admin/receipts/view.html', receipts=item_list)

def generate_pdf_custom():
    storage_dir = os.path.join(os.getcwd(), "app", "static", "storage", "file")
    output_pdf = os.path.join(storage_dir, "output.pdf")
    os.makedirs(storage_dir, exist_ok=True)

    item_list = inventory_service.get()
      

    # Render the HTML template with receipts data
    html_content = render_template("admin/receipts/generate.html", receipts=item_list)
    # return html_content
    try:
        process = subprocess.run(
            ["node", "node_scripts/generate_pdf.js", output_pdf],
            input=html_content,  # Pass HTML as input to Puppeteer
            text=True,
            capture_output=True,
            check=True
        )

        print(process.stdout)  # Debugging output
        # return send_file(output_pdf, as_attachment=True)
        return send_file(output_pdf, mimetype='application/pdf', as_attachment=False)

    except subprocess.CalledProcessError as e:
        return f"❌ Error generating PDF: {e}\n{e.stderr}"