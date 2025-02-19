from flask import Flask, render_template


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
    return render_template('admin/receipts.html', receipts=receipts)