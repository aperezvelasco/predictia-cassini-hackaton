import cdsapi
import os


def download_sea_ice_concentration(input_dir):
    """
    Function to download sea ice concentration data from the Climate Data Store (CDS)
    aggregated monthly using the CDS Toolbox.
    :return:
    """
    years_to_download = list(range(1980, 2021))
    years_to_download.reverse()
    for year_value in years_to_download:
        path_to_download = f"{input_dir}/{year_value}.nc"

        if os.path.exists(path_to_download):
            print(f'Data for {year_value} already exists at {path_to_download}')
            continue

        replacements = {
            'cdr_type_value': 'icdr' if year_value >= 2016 else 'cdr',
            'origin_value': 'eumetsat_osi_saf',
            'year_value': str(year_value)
        }
        with open("utilities/seaiceconc_download_workflow.py") as f:
            code = f.read()
        for key, value in replacements.items():
            code = code.replace(key, value)

        c = cdsapi.Client()
        print(f'Requesting data for {year_value} to {path_to_download}')
        r = c.workflow(code)
        print(f'Downloading data for {year_value} to {path_to_download}')
        c.download(r, targets=[path_to_download])