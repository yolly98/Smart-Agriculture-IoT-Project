This is a git-versioned subset of the Nordic Semiconductor nRF5 SDK

This repository's sole purpose is to provide the nRF5 SDK as a submodule for the [Contiki-NG Operating System](https://github.com/contiki-ng/contiki-ng/).

New versions will only appear in this repository only if and when Contiki-NG's nRF52840 port needs to use them.

Only the following folders have been kept:
* `components/boards`
* `components/drivers_nrf`
* `components/libraries`
* `integration/nrfx`
* `modules/nrfx`
* `documentation`
* `external/utf_converter`

All sources are and will remain otherwise intact, except in case where modifications are required by Contiki-NG.

The nRF5 SDK is distributed by Nordic Semiconductor [and is available for download here](https://www.nordicsemi.com/Software-and-tools/Software/nRF5-SDK). If you are looking for the latest version of the nRF5 SDK, do not clone this repository.

Do not open pulls / issues on this repository, unless they are immediately related to using the nRF52840 with Contiki-NG.

