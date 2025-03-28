from flask import Flask, render_template, make_response, send_file
import os
import subprocess


def receiptGenerate():
    receipts = [
            {
                'office_school': 'Magallanes District',
                'property_no': '12345',
                'date_acquired': '2023-01-01',
                'accountable_officer': 'Juan Dela Cruz'
            },
            {
                'office_school': 'Another School',
                'property_no': '67890',
                'date_acquired': '2023-02-01',
                'accountable_officer': 'Maria Santos'
            },
             {
                'office_school': 'Another School',
                'property_no': '67890',
                'date_acquired': '2023-02-01',
                'accountable_officer': 'Maria Santos'
            },
              {
                'office_school': 'Another School',
                'property_no': '67890',
                'date_acquired': '2023-02-01',
                'accountable_officer': 'Maria Santos'
            },
               {
                'office_school': 'Another School',
                'property_no': '67890',
                'date_acquired': '2023-02-01',
                'accountable_officer': 'Maria Santos'
            },
             {
                'office_school': 'Another School',
                'property_no': '67890',
                'date_acquired': '2023-02-01',
                'accountable_officer': 'Maria Santos'
            },
              {
                'office_school': 'Another School',
                'property_no': '67890',
                'date_acquired': '2023-02-01',
                'accountable_officer': 'Maria Santos'
            },
            # Add more receipts as needed
    ]
    return render_template('admin/receipts/view.html', receipts=receipts)

def generate_pdf_custom():
    storage_dir = os.path.join(os.getcwd(), "app", "static", "storage", "file")
    output_pdf = os.path.join(storage_dir, "output.pdf")
    os.makedirs(storage_dir, exist_ok=True)

    # Sample receipts data
    receipts = [
            {
                'office_school': 'Magallanes District',
                'property_no': '12345',
                'date_acquired': '2023-01-01',
                'accountable_officer': 'Juan Dela Cruz'
            },
            {
                'office_school': 'Another School',
                'property_no': '67890',
                'date_acquired': '2023-02-01',
                'accountable_officer': 'Maria Santos'
            },
             {
                'office_school': 'Another School',
                'property_no': '67890',
                'date_acquired': '2023-02-01',
                'accountable_officer': 'Maria Santos'
            },
              {
                'office_school': 'Another School',
                'property_no': '67890',
                'date_acquired': '2023-02-01',
                'accountable_officer': 'Maria Santos'
            },
               {
                'office_school': 'Another School',
                'property_no': '67890',
                'date_acquired': '2023-02-01',
                'accountable_officer': 'Maria Santos'
            },
             {
                'office_school': 'Another School',
                'property_no': '67890',
                'date_acquired': '2023-02-01',
                'accountable_officer': 'Maria Santos'
            },
              {
                'office_school': 'Another School',
                'property_no': '67890',
                'date_acquired': '2023-02-01',
                'accountable_officer': 'Maria Santos'
            },
            # Add more receipts as needed
    ]
   

    # Render the HTML template with receipts data
    html_content = render_template("admin/receipts/generate.html", receipts=receipts)
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