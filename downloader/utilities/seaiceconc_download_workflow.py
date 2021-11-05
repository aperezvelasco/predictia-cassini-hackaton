import cdstoolbox as ct


@ct.application(title='Download data')
@ct.output.download()
def application():
    data = ct.catalogue.retrieve(
        'satellite-sea-ice-concentration',
        {
            'origin': 'origin_value',
            'region': 'northern_hemisphere',
            'cdr_type': 'cdr_type_value',
            'year': 'year_value',
            'month': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
            ],
            'day': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
                '13', '14', '15',
                '16', '17', '18',
                '19', '20', '21',
                '22', '23', '24',
                '25', '26', '27',
                '28', '29', '30',
                '31',
            ],
            'version': 'v2',
            'variable': 'all',
        }
    )
    data = ct.cube.resample(data, freq='month', dim='time',
                            how='mean', keep_attrs=True, skipna=False)
    return data
