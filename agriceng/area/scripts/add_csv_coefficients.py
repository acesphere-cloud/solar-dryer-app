import csv

from agriceng.area.forms import CoefficientForm


def run(*args):
    with open('coefficients.csv',  mode='r') as rows:
        records_added = 0
        errors = []
        # Generate a dict per row, with the first CSV row being the keys
        for row in csv.DictReader(rows):
            # bind the row data to the CropForm
            form = CoefficientForm(row)
            # validate row data
            if form.is_valid():
                # save the crop record
                form.save()
                records_added += 1
            else:
                errors.append(form.errors)

        print(records_added)
        print(errors)
