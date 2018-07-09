import pytest
from telluric import GeoRaster2
from telluric.context import TelluricContext

from common_for_tests import (
    multi_raster_8b, sensor_bands_info,
    hyper_raster, hyper_raster_with_no_data,
    multi_raster_with_no_data, multi_raster_16b
)

from telluric.products import ProductsFactory


def test_multispectral_raster_gets_available_products():
    products = multi_raster_8b().get_products(sensor_bands_info())
    expected_products = ProductsFactory.get_matchings(multi_raster_8b().band_names, sensor_bands_info())
    assert products == expected_products


def test_hyperspectral_raster_gets_available_products():
    products = hyper_raster().get_products(sensor_bands_info())
    expected_products = ProductsFactory.get_matchings(hyper_raster().band_names, sensor_bands_info())
    assert products == expected_products


def test_multispectral_apply_product():
    raster = multi_raster_8b()
    for product_name in raster.get_products(sensor_bands_info()):
        if product_name == 'SingleBand':
            product = raster.apply(product_name, sensor_bands_info(), band=raster.band_names[0])
        else:
            product = raster.apply(product_name, sensor_bands_info())

        assert isinstance(product, GeoRaster2)


def test_hyper_apply_product():
    raster = hyper_raster()
    for product_name in raster.get_products(sensor_bands_info()):
        if product_name == 'SingleBand':
            product = raster.apply(product_name, sensor_bands_info(), band=raster.band_names[0])
        else:
            product = raster.apply(product_name, sensor_bands_info())

        assert isinstance(product, GeoRaster2)


@pytest.mark.parametrize("raster", [multi_raster_16b(),
                                    multi_raster_8b(),
                                    hyper_raster(),
                                    hyper_raster_with_no_data(),
                                    multi_raster_with_no_data()])
def test_it_visualized_to_colormap(raster):
    result = raster.apply('ndvi', sensor_bands_info()).visualize('cm-jet', vmax=1, vmin=-1)
    assert isinstance(result, GeoRaster2)
    assert result.band_names == ['red', 'green', 'blue']


@pytest.mark.parametrize("raster", [multi_raster_16b(),
                                    multi_raster_8b(),
                                    hyper_raster(),
                                    hyper_raster_with_no_data(),
                                    multi_raster_with_no_data()])
def test_it_visualized_to_default(raster):
    product = raster.apply('ndvi', sensor_bands_info(), metadata=True)
    result = product.raster.visualize(product.default_view, vmax=product.max, vmin=product.min)
    assert isinstance(result, GeoRaster2)
    assert result.band_names == ['red', 'green', 'blue']


@pytest.mark.parametrize("raster", [multi_raster_16b(),
                                    multi_raster_8b(),
                                    hyper_raster(),
                                    hyper_raster_with_no_data(),
                                    multi_raster_with_no_data()])
def test_use_context_manager_for_bands_info(raster):
    with TelluricContext(sensor_bands_info=sensor_bands_info()):
        result = raster.apply('ndvi').visualize('cm-jet', vmax=1, vmin=-1)
        assert isinstance(result, GeoRaster2)
        assert result.band_names == ['red', 'green', 'blue']
