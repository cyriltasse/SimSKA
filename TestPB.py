# PB stuff
# https://gitlab.com/ska-telescope/sdp/ska-sdp-func-python/-/blob/main/src/ska_sdp_func_python/imaging/primary_beams.py?ref_type=heads


# notebook examples
# https://gitlab.com/ska-telescope/ost/ska-ost-array-config/-/blob/master/docs/examples.ipynb

observation = simulate_observation(
    array_config=MidSubArray(subarray_type="AA*", exclude_stations="SKA008").array_config,
    phase_centre=phase_centre,
    start_time=9.6,
    duration=3600.0,
    integration_time=30,
    ref_freq=1420e6,
    chan_width=1e6,
    n_chan=10,
    horizon=20,
)

pixel_size = uvw.get_cellsize(over_sample=5)
model = generate_mfs_psf(
    observation, pixel_size, npixel=1024, weighting="robust", r_value=-1
)

beam = create_low_test_vp(
    model,
    use_local=False,
    azel=(numpy.deg2rad(az), numpy.deg2rad(el)),
)
