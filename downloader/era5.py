import xarray as xr
import numpy as np
import xesmf


def process_downloaded_era5(input_dir_tas, input_dir_seaiceconc, output_dir):
    years_to_download = list(range(1980, 2021))
    years_to_download.reverse()
    for year_value in years_to_download:
        print(f'Processing data for {year_value}')
        path_seaiceconc = f"{input_dir_seaiceconc}/{year_value}.nc"
        da_seaiceconc = xr.open_dataset(path_seaiceconc)
        da_seaiceconc = da_seaiceconc.rename({'x_laean': 'x', 'y_laean': 'y'})

        path_tas = f"{input_dir_tas}/tas_ERA5_{year_value}.nc"
        da_tas = xr.open_dataset(path_tas)
        da_tas = da_tas.resample(time='MS').mean()
        regridder_tas = xesmf.Regridder(
            da_tas, da_seaiceconc, method='bilinear'
        )
        regridded_tas = regridder_tas(da_tas)

        regridder_seaiconc = xesmf.Regridder(
            da_seaiceconc, regridded_tas, method='bilinear'
        )
        regridded_seaiceconc = regridder_seaiconc(da_seaiceconc)

        regridded_tas = regridded_tas.where(
            np.isnan(regridded_seaiceconc.siconca.isel(time=0))==False,
            drop=True
        )

        regridded_data = xr.merge([regridded_seaiceconc, regridded_tas])

        regridded_data.to_netcdf(f"{output_dir}/{year_value}.nc")
    return "Good"