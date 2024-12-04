from ska_ost_array_config.array_config import LowSubArray, MidSubArray
from casacore.tables import table, tableutil
import numpy


def createAntTable():

    low_aastar = LowSubArray(subarray_type="AA*")


    # bellow stollen from msv2.py in ska-sdp-datamodels
    nant,=low_aastar.array_config.names.shape

    col1 = tableutil.makearrcoldesc(
        "OFFSET",
        0.0,
        1,
        comment="Axes offset of mount to FEED REFERENCE point",
        keywords={
            "QuantumUnits": ["m", "m", "m"],
            "MEASINFO": {"type": "position", "Ref": "ITRF"},
        },
    )
    col2 = tableutil.makearrcoldesc(
        "POSITION",
        0.0,
        1,
        comment="Antenna X,Y,Z phase reference position",
        keywords={
            "QuantumUnits": ["m", "m", "m"],
            "MEASINFO": {"type": "position", "Ref": "ITRF"},
        },
    )
    col3 = tableutil.makescacoldesc(
        "TYPE",
        "ground-based",
        comment="Antenna type (e.g. SPACE-BASED)",
    )
    col4 = tableutil.makescacoldesc(
        "DISH_DIAMETER",
        2.0,
        comment="Physical diameter of dish",
        keywords={
            "QuantumUnits": [
                "m",
            ]
        },
    )
    col5 = tableutil.makescacoldesc(
        "FLAG_ROW", False, comment="Flag for this row"
    )
    col6 = tableutil.makescacoldesc(
        "MOUNT",
        "alt-az",
        comment="Mount type e.g. alt-az, equatorial, etc.",
    )
    col7 = tableutil.makescacoldesc(
        "NAME", "none", comment="Antenna name, e.g. VLA22, CA03"
    )


    siteName="SKA"
    col8 = tableutil.makescacoldesc(
        "STATION", siteName, comment="Station (antenna pad) name"
    )

    desc = tableutil.maketabdesc(
        [col1, col2, col3, col4, col5, col6, col7, col8]
    )


    tb = table("ANTENNA", desc, nrow=nant, ack=False)
    
    tb.putcol("OFFSET", numpy.zeros((nant, 3)), 0, nant)
    tb.putcol("TYPE", ["GROUND-BASED"] * nant, 0, nant)
    tb.putcol(
        "DISH_DIAMETER",
        [
            2.0,
        ]
        * nant,
        0,
        nant,
    )
    tb.putcol(
        "FLAG_ROW",
        [
            False,
        ]
        * nant,
        0,
        nant,
    )
    tb.putcol(
        "MOUNT",
        [
            "ALT-AZ",
        ]
        * nant,
        0,
        nant,
    )
    tb.putcol(
        "NAME",
        [ant.data[()] for ant in low_aastar.array_config.names],
        0,
        nant,
    )
    tb.putcol(
        "STATION",
        [
            siteName,
        ]
        * nant,
        0,
        nant,
    )

    for iAnt in range(nant):
        i=iAnt
        tb.putcell("OFFSET", i, [0.0, 0.0, 0.0])
        
        x,y,z=low_aastar.array_config.xyz[iAnt]
        x=x.data[()]
        y=y.data[()]
        z=z.data[()]
        tb.putcell(
            "POSITION",
            i,
            [
                x,
                y,
                z,
            ],
        )
        tb.putcell(
            "DISH_DIAMETER", i, low_aastar.array_config.diameter[i].data[()]
        )
        # tb.putcell('FLAG_ROW', i, False)
        tb.putcell("MOUNT", i, low_aastar.array_config.mount[i].data[()])
        tb.putcell("NAME", i, low_aastar.array_config.names[i].data[()])#ant.getName())
        tb.putcell("STATION", i, low_aastar.array_config.stations[i].data[()])
        # tb.putcell('STATION', i, self.siteName)

    tb.flush()
    tb.close()


def main():
    createAntTable()
    os.system("makems makems.cfg")
